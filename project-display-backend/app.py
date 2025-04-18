from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from create_db import create_database
from modules import *
from datetime import datetime
import pymysql
import bcrypt
import os
import threading

load_dotenv()
# 从配置文件中读取数据
MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST") # 数据库主机地址
MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER") # 数据库用户名
MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD") # 数据库密码
if not MYSQL_DATABASE_PASSWORD:
    exit()
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN") # 允许跨域的源
if ALLOW_ORIGIN:
    ALLOW_ORIGIN = ALLOW_ORIGIN.split(",")
    ALLOW_ORIGIN = [origin.strip() for origin in ALLOW_ORIGIN]
DOMAIN = os.getenv("DOMAIN") # 项目运行的 IPV4 地址
PER_PAGE_NUM = os.getenv("PER_PAGE_NUM") # 项目加载时，每页的数量
if not PER_PAGE_NUM:
    PER_PAGE_NUM = 15 # 默认 15
PER_PAGE_NUM = int(PER_PAGE_NUM)
TOKEN_INVALID_TIME = os.getenv("TOKEN_INVALID_TIME") # access-token 过期时间
if not TOKEN_INVALID_TIME:
    TOKEN_INVALID_TIME = 15 # 默认 15
TOKEN_INVALID_TIME = int(TOKEN_INVALID_TIME)

create_database()

# 数据库连接
db = pymysql.connect(
    host=MYSQL_DATABASE_HOST,
    user=MYSQL_DATABASE_USER,
    password=MYSQL_DATABASE_PASSWORD,
    db="project_display",
    charset="utf8mb4",
    autocommit=True
)
dbcursor = db.cursor()

# 创建一个线程锁对象，用于解决多个请求同时访问数据库问题
lock = threading.Lock()

app = Flask(__name__)

# 自定义允许跨域的源
CORS(app, resources={r"/*": {"origins": ALLOW_ORIGIN, "supports_credentials": True}})

# 在所有请求前判断数据库连接状态
@app.before_request
def before_request():
    if not db.open:
        db.connect()

# 处理前端登录请求
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # print(data)
    # 从用户表中查询用户， 并对密码作出判断
    sql = "SELECT * FROM `users` WHERE username = %s"
    val = (data['username'],)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        # 判断账户状态
        if result[0][7] == 0:
            return jsonify({'success': False, 'message': '该账号已被封禁', 'code': 200})
        if result[0][7] == 2:
            return jsonify({'success': False, 'message': '该账号已被注销', 'code': 200})
        # 将用户输入的密码转换为字节串
        user_password_bytes = data['password'].encode('utf-8')
        # 将数据库中的密码转换为字节串
        hashed_passowrd = result[0][2].encode('utf-8')
        # 使用 checkpw() 函数比较哈希值和用户输入的密码
        is_password_match = bcrypt.checkpw(
            user_password_bytes, hashed_passowrd)
        if is_password_match:
            # 生成accesstoken
            sql = "SELECT `nickname` FROM `user_info` WHERE `user_id` = %s"
            val = (result[0][0],)
            lock.acquire()
            dbcursor.execute(sql, val)
            lock.release()
            nickname = dbcursor.fetchall()
            if len(nickname) > 0:
                nickname = nickname[0][0]
            else:
                nickname = 'Unknown'
            access = f'${nickname}${result[0][0]}$'
            current_time = str(datetime.now())
            # 将 $用户名 $id$ 作为 front
            # 将时间戳加密, 作为 end
            # 将用户名及其 id 加密, 作为 center
            # 剪去 bcrypt 加密的标志
            token_end = bcrypt.hashpw(current_time.encode('utf-8'), bcrypt.gensalt())
            token_center = bcrypt.hashpw(access.encode('utf-8'), bcrypt.gensalt())
            accesstoken = access + token_center.decode('utf-8').split('$')[-1] + token_end.decode('utf-8').split('$')[-1]
            # print(accesstoken)
            # 将该用户原有的token删除
            sql = "DELETE FROM `access_token` WHERE `user_id` = %s"
            val = (result[0][0])
            lock.acquire()
            dbcursor.execute(sql, val)
            lock.release()
            db.commit()
            # 将accesstoken存入数据库
            sql = "INSERT INTO `access_token` (`user_id`, `token`) VALUES (%s, %s)"
            val = (result[0][0], accesstoken)
            lock.acquire()
            dbcursor.execute(sql, val)
            lock.release()
            db.commit()
            response = make_response(
                jsonify({'success': True, 'message': '登录成功', 'code': 200}))
            # 登录成功，配置前端 cookie
            response.set_cookie('access-token', accesstoken, domain=DOMAIN,
                                max_age=TOKEN_INVALID_TIME*24*3600, httponly=True) # type: ignore
            return response
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确', 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户名或密码不正确', 'code': 200})

# 处理前端注册请求
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # print(data)
    sql = "SELECT * FROM `users` WHERE username = %s"
    val = (data['username'],)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        return jsonify({'success': False, 'message': '注册失败\n用户名已存在', 'code': 200})
    else:
        # 进行用户名密码的合法化判断
        if not check_username(data['username']):
            return jsonify({'success': False, 'message': '注册失败\n用户名不合法', 'code': 200})
        if not check_password(data['password']):
            return jsonify({'success': False, 'message': '注册失败\n密码不合法', 'code': 200})
        if data['password'] != data['repassword']:
            return jsonify({'success': False, 'message': '注册失败\n两次输入密码不一致', 'code': 200})
        # 对用户的密码进行加密存储
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
        val = (data['username'], hashed_password)
        lock.acquire()
        dbcursor.execute(sql, val)
        lock.release()
        db.commit()
        return jsonify({'success': True, 'message': '注册成功', 'code': 200})

# 用于校验前端的登录状态
@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    # 获取前端携带的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    # 向前端返回当前的登录状态
    if check['success']:
        return jsonify({'success': True, 'data': '当前已登陆', 'code': 200})
    else:
        return jsonify({'success': False, 'data': '当前未登录', 'code': 200})
    
# 退出登录时，清楚前端的 cookie
@app.route('/clearCookie', methods=['POST'])
def clearCookie():
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        # 删除数据库中的 access-token 信息
        sql = "DELETE FROM `access_token` WHERE `token` = %s"
        val = (token)
        lock.acquire()
        dbcursor.execute(sql, val)
        lock.release()
        db.commit()
    response = make_response(jsonify({'success': True, 'message': '已登出', 'code': 200}))
    # 将前端的 cookie 设置为空
    response.set_cookie('access-token', '', expires=0, httponly=True)
    return response
    
# 返回 projects 数据
@app.route('/projects', methods=['POST'])
def projects():
    data = request.get_json()
    # print(data['page'], PER_PAGE_NUM * 2)
    sql = "SELECT * FROM `projects` ORDER BY `starred_num` DESC LIMIT %s OFFSET %s"
    val = (PER_PAGE_NUM, (data['page'] - 1) * PER_PAGE_NUM)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # print(result)
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    languages = dbcursor.fetchall()
    # 获取所有的用户信息
    sql = "SELECT * FROM `user_info`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    userinfos = dbcursor.fetchall()
    projectlist = []
    # 为每个项目，匹配对应的语言标签用户等信息
    for i in range(0, len(result)):
        # 初始化信息
        usericon = ''
        tags = []
        tagids = []
        language = {}
        # 将时间进行格式化
        updatetime = result[i][7].strftime('%Y/%m/%d')
        # 匹配用户信息，包括头像的 url
        for j in userinfos:
            if j[1] == result[i][1]:
                usericon = j[2]
                break
        # 匹配标签，一个项目可以有多个标签
        for x in projecttags:
            if x[1] == result[i][0]:
                tagids.append(x[2])
                for y in alltags:
                    if y[0] == x[2]:
                        tags.append(y[1])
                        break
        # 匹配语言，一个项目只有一个 main_language
        for m in languages:
            if m[0] == result[i][4]:
                language = {
                    'color': m[2],
                    'name': m[1]
                }
                break
        # 格式化项目信息
        project = {
            'id': result[i][0],
            'userid': result[i][1],
            'usericon': usericon,
            'name': result[i][2],
            'main': result[i][3],
            'cover': result[i][8],
            'tags': tags,
            'tagids': tagids,
            'language': language,
            'starnum': result[i][6],
            'updatetime': updatetime
        }
        # print(project)
        projectlist.append(project)

    return jsonify({'success': True, 'data': projectlist, 'code': 200})

# 返回 kinds 数据
@app.route('/kinds', methods=['GET'])
def kinds():
    sql = "SELECT * FROM `kinds`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    kinds = dbcursor.fetchall()
    kindlist = []
    # 定义返回的数据
    for i in kinds:
        kind = {
            'id': i[0],
            'name': i[1],
            'icon': i[2],
            'isactive': False
        }
        kindlist.append(kind)
    # print(kindlist[0]['isactive'])
    if len(kindlist) > 0:
        kindlist[0]['isactive'] = True
    
    return jsonify({'success': True, 'data': kindlist, 'code': 200})

# 返回 languages 数据
@app.route('/languages', methods=['GET'])
def languages():
    sql = "SELECT * FROM `languages` ORDER BY `language_hot` DESC"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    languages = dbcursor.fetchall()
    languagelist = []
    for i in languages:
        language = {
            'id': i[0],
            'name': i[1],
            'color': i[2],
            'isactive': False
        }
        languagelist.append(language)
    # print(kindlist[0]['isactive'])
    
    return jsonify({'success': True, 'data': languagelist, 'code': 200})

# 返回 tags 数据
@app.route('/tags', methods=['GET'])
def tags():
    sql = "SELECT * FROM `tags` ORDER BY `tag_hot` DESC"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    tags = dbcursor.fetchall()
    taglist = []
    for i in tags:
        language = {
            'id': i[0],
            'name': i[1],
            'isactive': False
        }
        taglist.append(language)
    # print(kindlist[0]['isactive'])
    
    return jsonify({'success': True, 'data': taglist, 'code': 200})

# 查询用户历史记录
@app.route('/history', methods=['POST'])
def get_history():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 获取用户的点赞记录
@app.route('/likes', methods=['POST'])
def get_likes():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 获取用户的关注列表
@app.route('/followed', methods=['POST'])
def get_followed():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400
    
# 获取用户的粉丝列表
@app.route('/following', methods=['POST'])
def get_following():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 更新用户个人资料
@app.route('/updateProfile', methods=['POST'])
def update_profile():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 获取用户的私信列表
@app.route('/messages', methods=['POST'])
def get_messages():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 创建私信
@app.route('/createMessage', methods=['POST'])
def create_message():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 发送私信
@app.route('/sendMessage', methods=['POST'])
def send_message():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400
    
# 更新私信
@app.route('/getMessage', methods=['POST'])
def get_message():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 查询特定文章的评论
@app.route('/comments', methods=['POST'])
def get_comments():
    if True:
        return jsonify({"status": "success", "message": "Message sent successfully"}), 201
    else:
        return jsonify({"status": "error", "message": "Message sending failed"}), 400

# 删除用户的某条评论
@app.route('/deleteComment', methods=['POST'])
def delete_comment():
    comment_id = request.json.get('comment_id')
    # 删除评论的数据库逻辑
    delete_status = # delete_comment_in_database(comment_id)
    if delete_status:
        return jsonify({"status": "success", "message": "Comment deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Comment deletion failed"}), 400


# 判断 access-token 是否有效
def checkCookie(token):
    # 判断当前 token 是否存在于数据库中
    sql = "SELECT * FROM `access_token` WHERE `token` = %s"
    val = (token,)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # 若数据库中存在当前 cookie, 判断其时间是否过期
    if len(result) > 0:
        current_time = datetime.now()  # type: ignore
        if isTimeOut(result[0][3], current_time):
            return ({'success': False, 'message': '登陆过期', 'code': 200})
        return  ({'success': True, 'message': '已登录', 'code': 200})
    else:
        return ({'success': False, 'message': '未登录', 'code': 200})

# 判断 cookie 是否过期
def isTimeOut(time1, time2):
    # 计算时间差值
    difference = abs(time2 - time1)
    # 判断差值是否大于 TOKEN_INVALID_TIME 天
    if difference.days >TOKEN_INVALID_TIME:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)