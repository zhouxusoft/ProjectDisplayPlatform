from flask import Flask, request, jsonify, make_response, g, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from create_db import create_database
from modules import *
from datetime import datetime
from werkzeug.utils import secure_filename
from ai import summary, explain
from collections import Counter
import pymysql
import bcrypt
import os
import threading
import uuid
import random

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
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") # 上传文件夹
if not UPLOAD_FOLDER:
    UPLOAD_FOLDER = "upload/"
MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH") # 上传文件大小限制
if not MAX_CONTENT_LENGTH:
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
MAX_CONTENT_LENGTH = int(MAX_CONTENT_LENGTH)
HOST = os.getenv("HOST")
if not HOST:
    HOST = "http://127.0.0.1:5000"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # 允许上传的文件类型

create_database()

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=MYSQL_DATABASE_HOST,
            user=MYSQL_DATABASE_USER,
            password=MYSQL_DATABASE_PASSWORD, # type: ignore
            db="project_display",
            charset="utf8mb4",
            autocommit=True
        ) # type: ignore
        g.cursor = g.db.cursor()
    return g.db, g.cursor

# 创建一个线程锁对象，用于解决多个请求同时访问数据库问题
lock = threading.Lock()

# app = Flask(__name__)
app = Flask(__name__, static_folder='../project-display-frontend/dist', static_url_path='')

@app.errorhandler(404)
def page_not_found(e):
    # 发生404错误时，重定向到根路径
    return send_from_directory(app.static_folder, 'index.html') # type: ignore

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html') # type: ignore

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 自定义允许跨域的源
CORS(app, resources={r"/*": {"origins": ALLOW_ORIGIN, "supports_credentials": True}})

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 文件上传接口
@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': '没有找到上传的文件'})

    file = request.files['image']
    result = saveFile(file)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result)

# 图片资源访问接口
@app.route('/uploads/<filename>')
def uploadedFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 处理前端登录请求
@app.route('/login', methods=['POST'])
def login():
    db, dbcursor = get_db()
    data = request.get_json()
    # print(data)
    # 从用户表中查询用户， 并对密码作出判断
    sql = "SELECT * FROM `users` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
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
            sql = "SELECT * FROM `user_info` WHERE `user_id` = %s"
            val = (result[0][0],)
            dbcursor.execute(sql, val)
            nickname = dbcursor.fetchall()
            if nickname[0][2] is None or nickname[0][2] == '':
                rand_num = random.randint(1, 10)
                icon = f'{rand_num}.png'
                path = os.path.join(HOST or '', app.config['UPLOAD_FOLDER'], icon)
                sql = "UPDATE `user_info` SET `user_icon` = %s WHERE `user_id` = %s"
                val = (path, result[0][0])
                dbcursor.execute(sql, val)
                db.commit()
            if len(nickname) > 0:
                nickname = nickname[0][3]
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
            val = (result[0][0],)
            dbcursor.execute(sql, val)
            db.commit()
            # 将accesstoken存入数据库
            sql = "INSERT INTO `access_token` (`user_id`, `token`) VALUES (%s, %s)"
            val = (result[0][0], accesstoken)
            dbcursor.execute(sql, val)
            db.commit()
            # 更新用户位置
            sql = "UPDATE `user_info` SET `position` = %s WHERE `user_id` = %s"
            val = (data['position'], result[0][0])
            dbcursor.execute(sql, val)
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
    db, dbcursor = get_db()
    data = request.get_json()
    # print(data)
    sql = "SELECT * FROM `users` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
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
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '注册成功', 'code': 200})

# 用于校验前端的登录状态
@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    db, dbcursor = get_db()
    # 获取前端携带的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    # 向前端返回当前的登录状态
    if check['success']:
        sql = "SELECT `nickname`, `user_icon` FROM `user_info` WHERE `user_id` = %s"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        userinfo = {
            'userid': check['userid'],
            'nickname': result[0][0],
            'usericon': result[0][1]
        }
        return jsonify({'success': True, 'data': '当前已登录', 'userinfo': userinfo, 'code': 200})
    else:
        return jsonify({'success': False, 'data': '当前未登录', 'code': 200})
    
# 退出登录时，清楚前端的 cookie
@app.route('/clearCookie', methods=['POST'])
def clearCookie():
    db, dbcursor = get_db()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        # 删除数据库中的 access-token 信息
        sql = "DELETE FROM `access_token` WHERE `token` = %s"
        val = (token)
        dbcursor.execute(sql, val)
        db.commit()
    response = make_response(jsonify({'success': True, 'message': '已登出', 'code': 200}))
    # 将前端的 cookie 设置为空
    response.set_cookie('access-token', '', expires=0, httponly=True)
    return response
    
# 返回 projects 数据
@app.route('/projects', methods=['POST'])
def projects():
    db, dbcursor = get_db()
    data = request.get_json()
    # print(data['page'], PER_PAGE_NUM * 2)
    if data['language'] == -1 and len(data['tags']) == 0:
        sql = "SELECT COUNT(*) FROM `projects`"
        dbcursor.execute(sql)
        total = dbcursor.fetchall()
        sql = "SELECT * FROM `projects` ORDER BY `starred_num` DESC LIMIT %s OFFSET %s"
        val = (PER_PAGE_NUM, (data['page'] - 1) * PER_PAGE_NUM)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    if data['language'] != -1 and len(data['tags']) == 0:
        sql = "SELECT COUNT(*) FROM `projects` WHERE `main_language_id` = %s"
        val = (data['language'],)
        dbcursor.execute(sql, val)
        total = dbcursor.fetchall()
        sql = "SELECT * FROM `projects` WHERE `main_language_id` = %s ORDER BY `starred_num` DESC LIMIT %s OFFSET %s"
        val = (data['language'], PER_PAGE_NUM, (data['page'] - 1) * PER_PAGE_NUM)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
    if data['language'] == -1 and len(data['tags']) != 0:
        tags = data['tags']
        tag_placeholders = ','.join(['%s'] * len(tags))

        count_sql = f"""
        SELECT COUNT(DISTINCT p.id)
        FROM projects p
        JOIN project_tag pt ON p.id = pt.project_id
        WHERE pt.tag_id IN ({tag_placeholders})
        """

        query_sql = f"""
        SELECT DISTINCT p.*
        FROM projects p
        JOIN project_tag pt ON p.id = pt.project_id
        WHERE pt.tag_id IN ({tag_placeholders})
        ORDER BY p.starred_num DESC
        LIMIT %s OFFSET %s
        """

        count_params = tags
        query_params = tags + [PER_PAGE_NUM, (data['page'] - 1) * PER_PAGE_NUM]

        dbcursor.execute(count_sql, count_params)
        total = dbcursor.fetchall()

        dbcursor.execute(query_sql, query_params)
        result = dbcursor.fetchall()
    # print(result)
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    dbcursor.execute(sql)
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    dbcursor.execute(sql)
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    dbcursor.execute(sql)
    languages = dbcursor.fetchall()
    # 获取所有的用户信息
    sql = "SELECT * FROM `user_info`"
    dbcursor.execute(sql)
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
            'updatetime': updatetime,
            'pagename': result[i][9],
            'circle': result[i][11],
        }
        # print(project)
        projectlist.append(project)

    return jsonify({'success': True, 'data': projectlist, 'total': total[0][0], 'code': 200})

# 返回 kinds 数据
@app.route('/kinds', methods=['GET'])
def kinds():
    db, dbcursor = get_db()
    sql = "SELECT * FROM `kinds`"
    dbcursor.execute(sql)
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
    
    return jsonify({'success': True, 'data': kindlist, 'code': 200})

# 返回 languages 数据
@app.route('/languages', methods=['GET'])
def languages():
    db, dbcursor = get_db()
    sql = "SELECT * FROM `languages` ORDER BY `language_hot` DESC"
    dbcursor.execute(sql)
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
    db, dbcursor = get_db()
    sql = "SELECT * FROM `tags` ORDER BY `tag_hot` DESC"
    dbcursor.execute(sql)
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

# 返回 文章详情 数据
@app.route('/projectDetail', methods=['POST'])
def projectDetail():
    db, dbcursor = get_db()
    data = request.get_json()
    token = request.cookies.get('access-token')
    # print(data['page'], PER_PAGE_NUM * 2)
    sql = "SELECT * FROM `projects` WHERE `page_name` = %s"
    val = (data['pagename'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 获取文章内容
    sql = "SELECT * FROM `project_readme` WHERE `project_id` = %s"
    val = (result[0][0],)
    dbcursor.execute(sql, val)
    readme = dbcursor.fetchall()
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    dbcursor.execute(sql)
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    dbcursor.execute(sql)
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    dbcursor.execute(sql)
    languages = dbcursor.fetchall()
    # 为项目，匹配对应的语言标签用户等信息
    tags = []
    tagids = []
    language = {}
    # 将时间进行格式化
    updatetime = result[0][7].strftime('%Y-%m-%d %H:%M:%S')
    loginInfo = checkCookie(token)
    if loginInfo['success']:
        my_id = loginInfo['userid']
    else:
        my_id = 0
    userinfo = getUserInfo(result[0][1], my_id)
    # 匹配标签，一个项目可以有多个标签
    for x in projecttags:
        if x[1] == result[0][0]:
            tagids.append(x[2])
            for y in alltags:
                if y[0] == x[2]:
                    tags.append(y[1])
                    break
    # 匹配语言，一个项目只有一个 main_language
    for m in languages:
        if m[0] == result[0][4]:
            language = {
                'color': m[2],
                'name': m[1]
            }
            break
    # 格式化项目信息
    project = {
        'id': result[0][0],
        'userid': result[0][1],
        'usericon': userinfo['usericon'],
        'name': result[0][2],
        'main': result[0][3],
        'cover': result[0][8],
        'tags': tags,
        'tagids': tagids,
        'language': language,
        'starnum': result[0][6],
        'updatetime': updatetime,
        'browsenum': result[0][10],
    }
    
    data = {
        'project': project,
        'readme': readme[0][2],
        'userinfo': userinfo
    }
    return jsonify({'success': True, 'data': data, 'code': 200})

# 返回 文章评论 数据
@app.route('/projectComments', methods=['POST'])
def projectComments():
    db, dbcursor = get_db()
    data = request.get_json()
    sql = "SELECT uc.id AS comment_id, uc.user_id, uc.project_id, uc.comment_content, uc.comment_time, uc.position, ui.user_icon, ui.nickname FROM project_display.user_comment uc LEFT JOIN project_display.user_info ui ON uc.user_id = ui.user_id WHERE uc.project_id = %s"
    val = (data['projectid'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    data = []
    for i in range(len(result)):
        project = {
            'commentid': result[i][0],
            'userid': result[i][1],
            'projectid': result[i][2],
            'content': result[i][3],
            'time': result[i][4].strftime('%Y-%m-%d %H:%M:%S'),
            'position': result[i][5],
            'usericon': result[i][6],
            'nickname': result[i][7],
        }
        data.append(project)
    return jsonify({'success': True, 'data': data, 'code': 200})

# 返回 用户ip 数据
@app.route('/get_ip', methods=['GET'])
def get_ip():
    return jsonify({
        'ip': get_client_ip(),
    })

# 进行评论
@app.route('/userComment', methods=['POST'])
def userComment():
    db, dbcursor = get_db()
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        # 获取当前用户的 id
        my_id = check['userid']
        sql = "INSERT INTO `user_comment` (`user_id`, `project_id`, `comment_content`, `position`) VALUES (%s, %s, %s, %s)"
        val = (my_id, data['projectid'], data['content'], data['position'])
        dbcursor.execute(sql, val)
        db.commit()
        
        sql = "SELECT `user_id` FROM `projects` WHERE `id` = %s"
        val = (data['projectid'])
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()[0][0]
        sql = "INSERT INTO `system_notification` (`user_id`, `notification_type`, `notification_content`) VALUES (%s, %s, %s)"
        val = (result, 2, data['projectid'])
        dbcursor.execute(sql, val)
        db.commit()
        
        return jsonify({'success': True, 'message': '评论成功', 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})

# 获取圈子列表
@app.route('/circleList', methods=['POST'])
def circleList():
    db, dbcursor = get_db()
    sql = """SELECT
        c.*,
        -- 统计成员数
        IFNULL(member_count.count, 0) AS member_count,
        -- 统计粉丝数
        IFNULL(follower_count.count, 0) AS follower_count,
        -- 统计作品数
        IFNULL(project_count.count, 0) AS project_count
        FROM
        circles c
        -- 左连接统计成员数 (type=0)
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM user_circle
            WHERE type = 0
            GROUP BY circle_id
        ) member_count ON member_count.circle_id = c.id
        -- 左连接统计粉丝数 (type=1)
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM user_circle
            WHERE type = 1
            GROUP BY circle_id
        ) follower_count ON follower_count.circle_id = c.id
        -- 左连接统计作品数
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM projects
            GROUP BY circle_id
        ) project_count ON project_count.circle_id = c.id
        ;
    """
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    # print(result)
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        sql = "SELECT `circle_id` FROM `user_circle` WHERE `user_id` = %s AND `type` = 0"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        userjoin = dbcursor.fetchall()
        userjoin = [row[0] for row in userjoin]
        sql = "SELECT `circle_id` FROM `user_circle` WHERE `user_id` = %s AND `type` = 1"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        userfollow = dbcursor.fetchall()
        userfollow = [row[0] for row in userfollow]
        sql = "SELECT `id` FROM `circles` WHERE `creater_id` = %s"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        usercreate = dbcursor.fetchall()
        usercreate = [row[0] for row in usercreate]
    else:
        userjoin = []
        userfollow = []
        usercreate = []
    # 整合结果
    circlelist = []
    for i in range(len(result)):
        # 0 无权限 1 创建者 2 成员 3 粉丝 4 路人
        flag = 0
        if result[i][0] in usercreate:
            flag = 1
        elif result[i][0] in userjoin:
            flag = 2
        elif result[i][0] in userfollow:
            flag = 3
        elif result[i][4] == 2:
            flag = 4
        circle = {
            'id': result[i][0],
            'creater_id': result[i][1],
            'name': result[i][2],
            'cover': result[i][3],
            'type': result[i][4],
            'description': result[i][5],
            'notice': result[i][6],
            'member_count': result[i][7],
            'follower_count': result[i][8],
            'project_count': result[i][9],
            'flag': flag
        }
        if flag != 0:
            circlelist.append(circle)
    return jsonify({'success': True, 'data': circlelist, 'code': 200})

# 获取用户列表
@app.route('/userList', methods=['POST'])
def userList():
    db, dbcursor = get_db()
    # print(data['page'], PER_PAGE_NUM * 2)
    sql = """
        SELECT
        ui.*,
        u.follower_num,
        u.following_num,
        IFNULL(p.project_count, 0) AS projects_num
        FROM
        user_info ui
        -- 关联 users 表获取粉丝数和关注数
        LEFT JOIN users u ON u.user_id = ui.user_id
        -- 统计 projects 作品数
        LEFT JOIN (
            SELECT user_id, COUNT(*) AS project_count
            FROM projects
            GROUP BY user_id
        ) p ON p.user_id = ui.user_id
    """
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        sql = "SELECT `follow_id` FROM `user_follow` WHERE `user_id` = %s"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        userfollowing = dbcursor.fetchall()
        userfollowing = [row[0] for row in userfollowing]
        sql = "SELECT `user_id` FROM `user_follow` WHERE `follow_id` = %s"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        userfollower = dbcursor.fetchall()
        userfollower = [row[0] for row in userfollower]
    else:
        userfollowing = []
        userfollower = []
    # 整合结果
    userlist = []
    for i in range(len(result)):
        flag = 0
        # 0 路人 1 我的粉丝 2 我的关注 3 相互关注 4 本人
        if result[i][1] == check['userid']:
            flag = 4
        elif result[i][1] in userfollower and result[i][1] in userfollowing:
            flag = 3
        elif result[i][1] in userfollowing:
            flag = 2
        elif result[i][1] in userfollower:
            flag = 1
        user = {
            'user_id': result[i][1],
            'usericon': result[i][2],
            'nickname': result[i][3],
            'bio': result[i][4],
            'position': result[i][5],
            'follower_num': result[i][6],
            'following_num': result[i][7],
            'projects_num': result[i][8],
            'flag': flag
        }
        if flag != 4:
            userlist.append(user)
    return jsonify({'success': True, 'data': userlist, 'code': 200})

# 关注用户
@app.route('/followUser', methods=['POST'])
def followUser():
    db, dbcursor = get_db()
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        # 判断当前用户是否已经关注该用户
        sql = "SELECT * FROM `user_follow` WHERE `user_id` = %s AND `follow_id` = %s"
        val = (check['userid'], data['userid'])
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        # 如果已经关注，则取关
        if len(result) > 0:
            # 1. 取消关注
            sql = "DELETE FROM `user_follow` WHERE `user_id` = %s AND `follow_id` = %s"
            val = (check['userid'], data['userid'])
            dbcursor.execute(sql, val)
            db.commit()
            return jsonify({'success': True, 'message': '取关成功', 'code': 200})
        sql = "INSERT INTO `user_follow` (`user_id`, `follow_id`) VALUES (%s, %s)"
        val = (check['userid'], data['userid'])
        dbcursor.execute(sql, val)
        db.commit()
        
        sql = "INSERT INTO `system_notification` (`user_id`, `notification_type`, `notification_content`) VALUES (%s, %s, %s)"
        val = (data['userid'], 3, check['userid'])
        dbcursor.execute(sql, val)
        db.commit()
        
        return jsonify({'success': True, 'message': '关注成功', 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})

# 返回圈子详情 数据
@app.route('/circleDetail', methods=['POST'])
def circleDetail():
    db, dbcursor = get_db()
    data = request.get_json()
    sql = """SELECT
        c.*,
        IFNULL(member_count.count, 0) AS member_count,
        IFNULL(follower_count.count, 0) AS follower_count,
        IFNULL(project_count.count, 0) AS project_count
        FROM
        circles c
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM user_circle
            WHERE type = 0
            GROUP BY circle_id
        ) member_count ON member_count.circle_id = c.id
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM user_circle
            WHERE type = 1
            GROUP BY circle_id
        ) follower_count ON follower_count.circle_id = c.id
        LEFT JOIN (
            SELECT circle_id, COUNT(*) AS count
            FROM projects
            GROUP BY circle_id
        ) project_count ON project_count.circle_id = c.id
        WHERE c.id = %s
        ;
    """
    val = (data['circleid'],)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchone()  # 只查一条

    if not result:
        # 没查到圈子，返回空或失败提示
        return jsonify({'success': False, 'message': '圈子不存在', 'code': 404})

    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if check['success']:
        user_id = check['userid']
        
        # 查询用户加入的圈子（成员 type=0）
        sql = "SELECT `circle_id` FROM `user_circle` WHERE `user_id` = %s AND `type` = 0"
        val = (user_id,)
        dbcursor.execute(sql, val)
        userjoin = [row[0] for row in dbcursor.fetchall()]

        # 查询用户关注的圈子（粉丝 type=1）
        sql = "SELECT `circle_id` FROM `user_circle` WHERE `user_id` = %s AND `type` = 1"
        val = (user_id,)
        dbcursor.execute(sql, val)
        userfollow = [row[0] for row in dbcursor.fetchall()]

        # 查询用户创建的圈子
        sql = "SELECT `id` FROM `circles` WHERE `creater_id` = %s"
        val = (user_id,)
        dbcursor.execute(sql, val)
        usercreate = [row[0] for row in dbcursor.fetchall()]
    else:
        userjoin = []
        userfollow = []
        usercreate = []

    # 计算权限标记
    flag = 0
    circle_id = result[0]
    circle_type = result[4]
    if circle_id in usercreate:
        flag = 1
    elif circle_id in userjoin:
        flag = 2
    elif circle_id in userfollow:
        flag = 3
    elif circle_type == 2:
        flag = 4

    circle = {
        'id': result[0],
        'creater_id': result[1],
        'name': result[2],
        'cover': result[3],
        'type': result[4],
        'description': result[5],
        'notice': result[6],
        'member_count': result[7],
        'follower_count': result[8],
        'project_count': result[9],
        'flag': flag
    }

    # 只有有权限才返回数据，或改成无权限也返回
    if flag == 0:
        return jsonify({'success': False, 'message': '无权限查看该圈子', 'code': 403})
    
    userlist = []
    if check['success']:
        userlist = getCircleUserList(circle_id, check['userid'])
    else:
        userlist = getCircleUserList(circle_id, 0)
        
    projectlist = getCircleProjectList(circle_id)

    return jsonify({'success': True, 'data': {'circle': circle, 'users': userlist, 'projects': projectlist}, 'code': 200})

# 返回我的个人信息
@app.route('/myInfo', methods=['POST'])
def myInfo():
    db, dbcursor = get_db()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    userinfo = {}
    projects = []
    if check['success']:
        projects = getUserProjectList(check['userid'])
        userinfo = getUserInfo(check['userid'], check['userid'])
    
        return jsonify({'success': True, 'data': { 'userinfo': userinfo, 'projects': projects }, 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})

# 获取用户的个人信息
@app.route('/userInfo', methods=['POST'])
def userInfo():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    userinfo = {}
    projects = []
    if check['success']:
        projects = getUserProjectList(data['userid'])
        userinfo = getUserInfo(data['userid'], check['userid'])
    
        return jsonify({'success': True, 'data': { 'userinfo': userinfo, 'projects': projects }, 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})

# 获取用户的点赞详细记录
@app.route('/userStarred', methods=['POST'])
def userStarred():
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        db, dbcursor = get_db()
        sql = "SELECT * FROM `projects`"
        dbcursor.execute(sql)
        allprojectlist = dbcursor.fetchall()
        sql = "SELECT * FROM `user_starred` WHERE `user_id` = %s"
        val = (check['userid'])
        dbcursor.execute(sql, val)
        userstarredlist = dbcursor.fetchall()
        userstarredprojects = []
        # 整合结果
        for i in range(0, len(userstarredlist)):
            for j in range(0, len(allprojectlist)):
                if userstarredlist[i][2] == allprojectlist[j][0]:
                    userstarredprojects.append(allprojectlist[j])
                    break
        projects = getProjectInfo(userstarredprojects)
        return jsonify({'success': True, 'data': projects, 'code': 200})
    else:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})

# 创建文章
@app.route('/createProject', methods=['POST'])
def createProject():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        pagename = generateUniquePagename()
        sql = "INSERT INTO `projects` (`user_id`, `project_name`, `project_overview`, `main_language_id`, `cover`, `page_name` , `circle_id`, `able_comment`, `able_look`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (check['userid'], data['project_name'], data['project_overview'], data['main_language_id'], data['cover'], pagename, data['circle_id'], data['able_comment'], data['able_look'])
        db, dbcursor = get_db()
        dbcursor.execute(sql, val)
        db.commit()
        
        project_id = dbcursor.lastrowid
        
        for tag_id in data['tags']:
            sql = "INSERT INTO `project_tag` (`project_id`, `tag_id`) VALUES (%s, %s)"
            val = (project_id, tag_id)
            dbcursor.execute(sql, val)
        sql = "INSERT INTO `project_readme` (`project_id`, `content`) VALUES (%s, %s)"
        val = (project_id, data['content'])
        dbcursor.execute(sql, val)
        db.commit()
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '文章发布失败', 'code': 400})
    
    return jsonify({'success': True, 'message': '文章发布成功', 'pagename': pagename, 'code': 200})

# 获取用户的点赞记录
@app.route('/starredList', methods=['POST'])
def starredList():
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if check['success']:
        db, dbcursor = get_db()
        sql = "SELECT * FROM `user_starred` WHERE `user_id` = %s"
        val = (check['userid'])
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        starlist = []
        for i in range(0, len(result)):
            item = {
                'id': result[i][0],
                'projectid': result[i][2],
                'starredtime': result[i][3].strftime('%Y-%m-%d %H:%M:%S')
            }
            starlist.append(item)
        return jsonify({'success': True, 'data': starlist, 'code': 200})
    else:
        return jsonify({'success': True, 'data': [], 'code': 200})

# 用户点赞
@app.route('/starProject', methods=['POST'])
def starProject():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    db, dbcursor = get_db()
    # 判断是否已经点赞
    sql = "SELECT * FROM `user_starred` WHERE `user_id` = %s AND `project_id` = %s"
    val = (check['userid'], data['project_id'])
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    if len(result) > 0:
        sql = "DELETE FROM `user_starred` WHERE `user_id` = %s AND `project_id` = %s"
        val = (check['userid'], data['project_id'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '取消点赞', 'code': 200})
    else:
        sql = "INSERT INTO `user_starred` (`user_id`, `project_id`) VALUES (%s, %s)"
        val = (check['userid'], data['project_id'])
        db, dbcursor = get_db()
        dbcursor.execute(sql, val)
        db.commit()
        
        sql = "SELECT `user_id` FROM `projects` WHERE `id` = %s"
        val = (data['project_id'])
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()[0][0]
        sql = "INSERT INTO `system_notification` (`user_id`, `notification_type`, `notification_content`) VALUES (%s, %s, %s)"
        val = (result, 1, data['project_id'])
        dbcursor.execute(sql, val)
        db.commit()
        
        return jsonify({'success': True, 'message': '点赞成功', 'code': 200})
    
# 更新用户个人资料
@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "UPDATE `user_info` SET `nickname` = %s, `user_icon` = %s, `bio` = %s WHERE `user_id` = %s"
        val = (data['nickname'], data['usericon'], data['bio'], check['userid'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '更新成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '更新失败', 'code': 400})

# 创建圈子
@app.route('/createCircle', methods=['POST'])
def createCircle():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "SELECT * FROM `circles` WHERE `name` = %s"
        val = (data['name'],)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        if len(result) > 0:
            return jsonify({'success': False, 'message': '圈子名称重复', 'code': 400})
        
        sql = "INSERT INTO `circles` (`creater_id`, `name`, `cover`, `description`, `type`) VALUES (%s, %s, %s, %s, %s)"
        val = (check['userid'], data['name'], data['cover'], data['description'], data['type'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '创建成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '创建失败', 'code': 400})

# 获取私信用户列表
@app.route('/messageUser', methods=['POST'])
def messageUser():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "SELECT * FROM `user_message` WHERE `sender_id` = %s OR `receiver_id` = %s"
        val = (check['userid'], check['userid'])
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        
        messageList = []
        for i in result:
            messageItem = {
                'id': i[0],
                'sender_id': i[1],
                'receiver_id': i[2],
                'type': i[3],
                'content': i[4],
                'send_time': i[5].strftime('%Y-%m-%d %H:%M:%S'),
                'read': i[6]
            }
            messageList.append(messageItem)
        
        chatUserIdList = []
        tempresult = result[::-1]
        for i in tempresult:
            if i[1] == check['userid']:
                chatUserIdList.append(i[2])
            else:
                chatUserIdList.append(i[1])
        chatUserIdList = list(dict.fromkeys(chatUserIdList))
        chatUserList = []
        for i in chatUserIdList:
            chatUser = getChatUserInfo(i, check['userid'])
            chatUserList.append(chatUser)
        if len(result) > 0:
            return jsonify({'success': True, 'data': messageList, 'chartUserList': chatUserList, 'code': 200})
        else:
            return jsonify({'success': True, 'data': [], 'chartUserList': [], 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '获取私信记录失败', 'code': 400})

# 阅读用户私信
@app.route('/readMessage', methods=['POST'])
def readMessage():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "UPDATE `user_message` SET `is_read` = 1 WHERE `sender_id` = %s AND `receiver_id` = %s"
        val = (data['userid'], check['userid'])
        dbcursor.execute(sql, val)
        sql = "UPDATE `user_message` SET `is_read` = 1 WHERE `sender_id` = %s AND `receiver_id` = %s"
        val = (check['userid'], data['userid'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '更新成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '更新失败', 'code': 400})

# 发送私信
@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "INSERT INTO `user_message` (`sender_id`, `receiver_id`, `message_type`, `message_content`) VALUES (%s, %s, %s, %s)"
        val = (check['userid'], data['userid'], data['type'], data['content'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '发送成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '发送失败', 'code': 400})

# 名词解释
@app.route('/explainText', methods=['POST'])
def explainText():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        answer = explain(data['text'])
        return jsonify({'success': True, 'message': answer.content, 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '解释失败', 'code': 400})
    
# 总结文本
@app.route('/summarizeText', methods=['POST'])
def summarizeText():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        answer = summary(data['text'])
        return jsonify({'success': True, 'message': answer.content, 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '总结失败', 'code': 400})

# 更新圈子信息
@app.route('/updateCircle', methods=['POST'])
def updateCircle():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "UPDATE `circles` SET `description` = %s, `cover` = %s, `notice` = %s  WHERE `id` = %s"
        val = (data['description'], data['cover'], data['notice'], data['circleid'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '更新成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '更新失败', 'code': 400})

# 获取可邀请列表
@app.route('/inviteUserList', methods=['POST'])
def inviteUserList():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "SELECT `user_id` FROM `user_circle` WHERE `circle_id`= %s"
        val = (data['circleid'],)
        dbcursor.execute(sql, val)
        circleuseridlist = dbcursor.fetchall()
        sql = "SELECT `follow_id` FROM `user_follow` WHERE `user_id`= %s"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        followuseridlist = dbcursor.fetchall()
        
        # 提取ID集合
        circle_ids = set(user_id[0] for user_id in circleuseridlist)
        follow_ids = set(follow_id[0] for follow_id in followuseridlist)

        # 求差集
        diff_ids = follow_ids - circle_ids
        
        invitelist = []
        for id in diff_ids:
            invitelist.append(getUserInfo(id, check['userid']))
        
        return jsonify({'success': True, 'data': invitelist, 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '获取失败', 'code': 400})

# 订阅圈子
@app.route('/orderCircle', methods=['POST'])
def orderCircle():
    data = request.get_json()
    # 获取前端的 cookie
    token = request.cookies.get('access-token')
    # 判断该 cookie 是否有效
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        # 判断用户是否已经订阅过该圈子
        db, dbcursor = get_db()
        sql = "SELECT `circle_id` FROM `user_circle` WHERE `user_id` = %s AND `circle_id` = %s"
        val = (check['userid'], data['circleid'])
        dbcursor.execute(sql, val)
        circleid = dbcursor.fetchone()
        if circleid != None:
            # 取消订阅
            sql = "DELETE FROM `user_circle` WHERE `user_id` = %s AND `circle_id` = %s AND `type` = 1"
            val = (check['userid'], data['circleid'])
            dbcursor.execute(sql, val)
            db.commit()
            return jsonify({'success': True, 'message': '取消订阅', 'code': 200})
        db, dbcursor = get_db()
        sql = "INSERT INTO `user_circle` (`user_id`, `circle_id`, `type`) VALUES (%s, %s, %s)"
        val = (check['userid'], data['circleid'], 1)
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '订阅成功', 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '订阅失败', 'code': 400})

# 获取未读私信数量
@app.route('/unreadMessageNum', methods=['POST'])
def unreadMessageNum():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    try:
        db, dbcursor = get_db()
        sql = "SELECT COUNT(*) FROM `user_message` WHERE `receiver_id` = %s AND `is_read` = 0"
        val = (check['userid'],)
        dbcursor.execute(sql, val)
        num = dbcursor.fetchall()[0][0]
        return jsonify({'success': True, 'data': num, 'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '获取失败', 'code': 400})

# 获取用户系统通知
@app.route('/systemMessage', methods=['POST'])
def systemMessage():
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    # 1：点赞
    # 2：评论
    # 3：关注
    # 4：被移除
    # 5：被邀请
    db, dbcursor = get_db()
    sql = "SELECT * FROM `system_notification` WHERE `user_id` = %s AND `is_read` = 0 AND `notification_type` = 1"
    val = (check['userid'],)
    dbcursor.execute(sql, val)
    starresult = dbcursor.fetchall()
    starmessage = listToCountDict([int(result[3]) for result in starresult])
    for item in starmessage:
        sql = "SELECT `project_name`, `page_name` FROM `projects` WHERE `id` = %s"
        val = (item['id'],)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        item['project_name'] = result[0][0]
        item['page_name'] = result[0][1]
    
    sql = "SELECT * FROM `system_notification` WHERE `user_id` = %s AND `is_read` = 0 AND `notification_type` = 2"
    val = (check['userid'],)
    dbcursor.execute(sql, val)
    commentresult = dbcursor.fetchall()
    commentmessage = listToCountDict([int(result[3]) for result in commentresult])
    for item in commentmessage:
        sql = "SELECT `project_name`, `page_name` FROM `projects` WHERE `id` = %s"
        val = (item['id'],)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        item['project_name'] = result[0][0]
        item['page_name'] = result[0][1]

    sql = "SELECT * FROM `system_notification` WHERE `user_id` = %s AND `is_read` = 0 AND `notification_type` = 3"
    val = (check['userid'],)
    dbcursor.execute(sql, val)
    followresult = dbcursor.fetchall()
    followmessage = len(followresult)
    
    sql = "SELECT * FROM `system_notification` WHERE `user_id` = %s AND `is_read` = 0 AND `notification_type` = 4"
    val = (check['userid'],)
    dbcursor.execute(sql, val)
    inviteresult = dbcursor.fetchall()
    invitemessage = []
    for item in inviteresult:
        invitemessageitem = {}
        user = int(item[3].split(',')[0])
        circle = int(item[3].split(',')[1])
        sql = "SELECT `name` FROM `circles` WHERE `id` = %s"
        val = (circle,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        invitemessageitem['circle_name'] = result[0][0]
        res = getUserInfo(user)
        invitemessageitem['nickname'] = res['nickname']
        invitemessageitem['circle_id'] = circle
        invitemessageitem['user_id'] = user
        invitemessageitem['id'] = item[0]
        invitemessage.append(invitemessageitem)
        
    sql = "SELECT * FROM `system_notification` WHERE `user_id` = %s AND `is_read` = 0 AND `notification_type` = 5"
    val = (check['userid'],)
    dbcursor.execute(sql, val)
    removeresult = dbcursor.fetchall()
    removemessage = []
    for item in removeresult:
        removemessageitem = {}
        circle = int(item[3])
        sql = "SELECT `name` FROM `circles` WHERE `id` = %s"
        val = (circle,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        removemessageitem['circle_name'] = result[0][0]
        removemessageitem['circle_id'] = circle
        removemessageitem['id'] = item[0]
        removemessage.append(removemessageitem)
    
    allmessage = {
        'star': starmessage,
        'comment': commentmessage,
        'follow': followmessage,
        'invite': invitemessage,
        'remove': removemessage
    }
    
    return jsonify({'success': True, 'data': allmessage, 'code': 200})

# 用户已读通知
@app.route('/readSystemMessage', methods=['POST'])
def readSystemMessage():
    data = request.get_json()
    token = request.cookies.get('access-token')
    check = checkCookie(token)
    if not check['success']:
        return jsonify({'success': False, 'message': '用户未登录', 'code': 401})
    
    db, dbcursor = get_db()
    if data['type'] == 1:
        sql = "UPDATE `system_notification` SET `is_read` = 1 WHERE `user_id` = %s AND `notification_type` = 1 AND `notification_content` = %s"
        val = (check['userid'], data['content'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'code': 200})
    
    if data['type'] == 2:
        sql = "UPDATE `system_notification` SET `is_read` = 1 WHERE `user_id` = %s AND `notification_type` = 2 AND `notification_content` = %s"
        val = (check['userid'], data['content'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'code': 200})
    
    if data['type'] == 3:
        sql = "UPDATE `system_notification` SET `is_read` = 1 WHERE `user_id` = %s AND `notification_type` = 3"
        val = (check['userid'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'code': 200})
    
    if data['type'] == 4:
        sql = "UPDATE `system_notification` SET `is_read` = 1 WHERE `id` = %s"
        val = (data['content'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'code': 200})
    
    if data['type'] == 5:
        sql = "UPDATE `system_notification` SET `is_read` = 1 WHERE `id` = %s"
        val = (data['content'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'code': 200})
    
    return jsonify({'success': False, 'message': '参数错误', 'code': 400})

def get_client_ip():
    ip = ""
    if request.headers.getlist("X-Forwarded-For"):
        ip_segment = request.headers.getlist("X-Forwarded-For")[0] or ""
        ip = ip_segment.split(',')[0]
    else:
        ip = request.remote_addr or ""  # 处理潜在None值
    return ip.strip()

# 获取用户个人信息
def getUserInfo(user_id, my_id=0):
    db, dbcursor = get_db()
    # 获取用户信息
    sql = "SELECT * FROM `user_info` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 获取用户粉丝数量
    sql = "SELECT COUNT(*) FROM `user_follow` WHERE `follow_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    follower = dbcursor.fetchall()[0][0]
    # 获取用户关注数量
    sql = "SELECT COUNT(*) FROM `user_follow` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    following = dbcursor.fetchall()[0][0]
    # 获取用户作品数量
    sql = "SELECT COUNT(*) FROM `projects` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    projectnum = dbcursor.fetchall()[0][0]
    # 获取用户与当前用户的关系
    if my_id != 0 and int(my_id) != int(user_id):
        sql = "SELECT * FROM `user_follow` WHERE `user_id` = %s AND `follow_id` = %s"
        val = (my_id, user_id)
        dbcursor.execute(sql, val)
        result2 = dbcursor.fetchall()
        if len(result2) > 0:
            relationship = 1
            # 互相关注
            sql = "SELECT * FROM `user_follow` WHERE `user_id` = %s AND `follow_id` = %s"
            val = (user_id, my_id)
            dbcursor.execute(sql, val)
            result2 = dbcursor.fetchall()
            if len(result2) > 0:
                relationship = 2
        else:
            relationship = 0
    elif int(my_id) == int(user_id):
        relationship = -1
    else:
        relationship = 0
        
    return {
        'user_id': result[0][1],
        'nickname': result[0][3],
        'usericon': result[0][2],
        'bio': result[0][4],
        'position': result[0][5],
        'follower': follower,
        'following': following,
        'projectnum': projectnum,
        'relationship': relationship # -1: 本人, 0: 未关注, 1: 已关注, 2: 相互关注
    }

# 获取聊天用户的个人信息
def getChatUserInfo(user_id, my_id=0):
    db, dbcursor = get_db()
    # 获取用户信息
    sql = "SELECT * FROM `user_info` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 获取用户粉丝数量
    sql = "SELECT COUNT(*) FROM `user_follow` WHERE `follow_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    follower = dbcursor.fetchall()[0][0]
    # 获取用户关注数量
    sql = "SELECT COUNT(*) FROM `user_follow` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    following = dbcursor.fetchall()[0][0]
    # 获取用户作品数量
    sql = "SELECT COUNT(*) FROM `projects` WHERE `user_id` = %s"
    val = (user_id,)
    dbcursor.execute(sql, val)
    projectnum = dbcursor.fetchall()[0][0]
    flag = 0
    # 获取用户与当前用户的关系
    if my_id != 0 and int(my_id) != int(user_id):
        sql = "SELECT `follow_id` FROM `user_follow` WHERE `user_id` = %s"
        val = (my_id,)
        dbcursor.execute(sql, val)
        userfollowing = dbcursor.fetchall()
        userfollowing = [row[0] for row in userfollowing]
        sql = "SELECT `user_id` FROM `user_follow` WHERE `follow_id` = %s"
        val = (my_id,)
        dbcursor.execute(sql, val)
        userfollower = dbcursor.fetchall()
        userfollower = [row[0] for row in userfollower]
        # 0 路人 1 我的粉丝 2 我的关注 3 相互关注
        if user_id in userfollower and user_id in userfollowing:
            flag = 3
        elif user_id in userfollowing:
            flag = 2
        elif user_id in userfollower:
            flag = 1
    
    sql = "SELECT COUNT(*) FROM `user_message` WHERE `sender_id` = %s AND `receiver_id` = %s AND `is_read` = 0"
    val = (user_id, my_id)
    dbcursor.execute(sql, val)
    unreadnum = dbcursor.fetchall()[0][0]

    return {
        'user_id': result[0][1],
        'nickname': result[0][3],
        'usericon': result[0][2],
        'bio': result[0][4],
        'position': result[0][5],
        'follower': follower,
        'following': following,
        'projectnum': projectnum,
        'relationship': flag, # 0 路人 1 我的粉丝 2 我的关注 3 相互关注
        'unreadnum': unreadnum
    }

# 获取圈子的用户列表
def getCircleUserList(circleid, my_id=0):
    db, dbcursor = get_db()
    userlist = []
    # 查询圈子创建者id
    sql = "SELECT `creater_id` FROM `circles` WHERE `id` = %s"
    val = (circleid,)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    if len(result) == 0:
        return []
    createrid = result[0][0]
    # 查询创建者信息
    createrInfo = {}
    createrInfo = getUserInfo(createrid, my_id)
    createrInfo['role'] = 'creater'
    createrInfo['follower_num'] = createrInfo['follower']
    createrInfo['following_num'] = createrInfo['following']
    createrInfo['projects_num'] = createrInfo['projectnum']
    createrInfo['flag'] = createrInfo['relationship']
    if createrInfo['flag'] == -1:
        createrInfo['flag'] = 4
    userlist.append(createrInfo)
    
    # 查询该圈子所有成员（type=0
    sql = """
        SELECT
            ui.*,
            u.follower_num,
            u.following_num,
            IFNULL(p.project_count, 0) AS projects_num,
            uc.type
        FROM user_circle uc
        JOIN user_info ui ON ui.user_id = uc.user_id
        LEFT JOIN users u ON u.user_id = ui.user_id
        LEFT JOIN (
            SELECT user_id, COUNT(*) AS project_count
            FROM projects
            GROUP BY user_id
        ) p ON p.user_id = ui.user_id
        WHERE uc.circle_id = %s AND (uc.type = 0 OR uc.user_id = %s)
    """
    # 这里保证查询圈子成员（type=0）和创建者（uc.user_id=circles.creater_id）
    dbcursor.execute(sql, (circleid, createrid))
    users_result = dbcursor.fetchall()

    # 查询当前用户的粉丝和关注，用于判断flag
    if my_id != 0:
        user_id = my_id
        sql = "SELECT follow_id FROM user_follow WHERE user_id = %s"
        dbcursor.execute(sql, (user_id,))
        userfollowing = [row[0] for row in dbcursor.fetchall()]
        sql = "SELECT user_id FROM user_follow WHERE follow_id = %s"
        dbcursor.execute(sql, (user_id,))
        userfollower = [row[0] for row in dbcursor.fetchall()]
    else:
        userfollowing = []
        userfollower = []

    for row in users_result:
        # row 对应字段如下（按你SQL字段顺序）：
        # ui.* 假设：id(0), user_id(1), usericon(2), nickname(3), bio(4), position(5), ...
        # u.follower_num(6), u.following_num(7), projects_num(8), uc.type(9)

        # 判断关注标识 flag，0 路人 1 我的粉丝 2 我的关注 3 相互关注 4 本人
        uf = 0
        this_user_id = row[1]
        if my_id != 0:
            user_id = my_id
            if this_user_id == user_id:
                uf = 4
            elif this_user_id in userfollower and this_user_id in userfollowing:
                uf = 3
            elif this_user_id in userfollowing:
                uf = 2
            elif this_user_id in userfollower:
                uf = 1

        role = 'member'

        user = {
            'user_id': row[1],
            'usericon': row[2],
            'nickname': row[3],
            'bio': row[4],
            'position': row[5],
            'follower_num': row[6],
            'following_num': row[7],
            'projects_num': row[8],
            'flag': uf,
            'role': role
        }

        userlist.append(user)
    return userlist

# 获取圈子项目信息列表
def getCircleProjectList(circleid, my_id=0):
    db, dbcursor = get_db()
    sql = "SELECT * FROM `projects` WHERE `circle_id` = %s ORDER BY `starred_num`"
    val = (circleid, )
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # print(result)
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    dbcursor.execute(sql)
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    dbcursor.execute(sql)
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    dbcursor.execute(sql)
    languages = dbcursor.fetchall()
    # 获取所有的用户信息
    sql = "SELECT * FROM `user_info`"
    dbcursor.execute(sql)
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
            'updatetime': updatetime,
            'pagename': result[i][9],
            'circle': result[i][11],
        }
        # print(project)
        projectlist.append(project)
    return projectlist

# 获得用户的项目信息列表
def getUserProjectList(userid, my_id=0):
    db, dbcursor = get_db()
    sql = "SELECT * FROM `projects` WHERE `user_id` = %s ORDER BY `starred_num`"
    val = (userid, )
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # print(result)
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    dbcursor.execute(sql)
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    dbcursor.execute(sql)
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    dbcursor.execute(sql)
    languages = dbcursor.fetchall()
    # 获取所有的用户信息
    sql = "SELECT * FROM `user_info`"
    dbcursor.execute(sql)
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
            'updatetime': updatetime,
            'pagename': result[i][9],
            'circle': result[i][11],
        }
        # print(project)
        projectlist.append(project)
    return projectlist

# 根据项目列表返回项目详细信息
def getProjectInfo(projects):
    db, dbcursor = get_db()
    # 获取所有的标签
    sql = "SELECT * FROM `tags`"
    dbcursor.execute(sql)
    alltags = dbcursor.fetchall()
    # 获取所有的项目对应的标签
    sql = "SELECT * FROM `project_tag`"
    dbcursor.execute(sql)
    projecttags = dbcursor.fetchall()
    # 获取所有的语言
    sql = "SELECT * FROM `languages`"
    dbcursor.execute(sql)
    languages = dbcursor.fetchall()
    # 获取所有的用户信息
    sql = "SELECT * FROM `user_info`"
    dbcursor.execute(sql)
    userinfos = dbcursor.fetchall()
    projectlist = []
    # 为每个项目，匹配对应的语言标签用户等信息
    for i in range(0, len(projects)):
        # 初始化信息
        usericon = ''
        tags = []
        tagids = []
        language = {}
        # 将时间进行格式化
        updatetime = projects[i][7].strftime('%Y/%m/%d')
        # 匹配用户信息，包括头像的 url
        for j in userinfos:
            if j[1] == projects[i][1]:
                usericon = j[2]
                break
        # 匹配标签，一个项目可以有多个标签
        for x in projecttags:
            if x[1] == projects[i][0]:
                tagids.append(x[2])
                for y in alltags:
                    if y[0] == x[2]:
                        tags.append(y[1])
                        break
        # 匹配语言，一个项目只有一个 main_language
        for m in languages:
            if m[0] == projects[i][4]:
                language = {
                    'color': m[2],
                    'name': m[1]
                }
                break
        # 格式化项目信息
        project = {
            'id': projects[i][0],
            'userid': projects[i][1],
            'usericon': usericon,
            'name': projects[i][2],
            'main': projects[i][3],
            'cover': projects[i][8],
            'tags': tags,
            'tagids': tagids,
            'language': language,
            'starnum': projects[i][6],
            'updatetime': updatetime,
            'pagename': projects[i][9],
            'circle': projects[i][11],
        }
        # print(project)
        projectlist.append(project)
    return projectlist

# 判断 access-token 是否有效
def checkCookie(token):
    db, dbcursor = get_db()
    # 判断当前 token 是否存在于数据库中
    sql = "SELECT * FROM `access_token` WHERE `token` = %s"
    val = (token,)
    dbcursor.execute(sql, val)
    result = dbcursor.fetchall()
    # 若数据库中存在当前 cookie, 判断其时间是否过期
    if len(result) > 0:
        current_time = datetime.now()  # type: ignore
        if isTimeOut(result[0][3], current_time):
            return ({'success': False, 'message': '登录过期', 'code': 200})
        return  ({'success': True, 'message': '已登录', 'userid': result[0][1], 'code': 200})
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

# 判断文件类型是否合法
def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 生成短的 uuid
def shortUuid(length=8):
    return uuid.uuid4().hex[:length].upper()

# 生成不重复的页面名
def generateUniquePagename():
    while True:
        pagename = shortUuid(8)
        db, dbcursor = get_db()
        sql = "SELECT * FROM `projects` WHERE `page_name` = %s"
        val = (pagename,)
        dbcursor.execute(sql, val)
        result = dbcursor.fetchall()
        if len(result) == 0:
            return pagename

# 生成唯一的文件名
def generateUniqueFilename(filename):
    ext = os.path.splitext(filename)[1]
    if not ext:
        # 如果没有扩展名，默认用 .jpg 或返回错误
        ext = '.jpg'  # 或 raise 异常
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

# 算出数组每一项的重复次数
def listToCountDict(lst):
    counter = Counter(lst)
    result = [{'id': k, 'num': v} for k, v in counter.items()]
    return result

# 保存上传的文件
def saveFile(file):
    if file.filename == '':
        return {'success': False, 'message': '未选择文件'}

    if not allowedFile(file.filename):
        return {'success': False, 'message': '文件格式不支持'}

    filename = file.filename
    unique_filename = generateUniqueFilename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    fullpath = os.path.join(HOST or '', app.config['UPLOAD_FOLDER'], unique_filename)
    try:
        file.save(filepath)
        return {'success': True, 'message': '上传成功', 'filename': unique_filename, 'filepath': fullpath}
    except Exception as e:
        return {'success': False, 'message': f'保存文件失败: {e}'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)