from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from create_db import create_database
from modules import *
import pymysql
import bcrypt
import os
import threading
import random

load_dotenv()
# 从配置文件中读取数据
MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST")
MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER")
MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD")
if not MYSQL_DATABASE_PASSWORD:
    exit()
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN")
if ALLOW_ORIGIN:
    ALLOW_ORIGIN = ALLOW_ORIGIN.split(",")
    ALLOW_ORIGIN = [origin.strip() for origin in ALLOW_ORIGIN]
DOMAIN = os.getenv("DOMAIN")
PER_PAGE_NUM = os.getenv("PER_PAGE_NUM")
if not PER_PAGE_NUM:
    PER_PAGE_NUM = 15
PER_PAGE_NUM = int(PER_PAGE_NUM)


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

def random_color():
    color = '{:06x}'.format(random.randint(0, 0xFFFFFF))
    return color

# 在所有请求前判断数据库连接状态
@app.before_request
def before_request():
    if not db.open:
        db.connect()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # print(data)
    # 从用户表中查询用户， 并对密码作出判断
    sql = "SELECT * FROM `users` WHERE username = ?"
    val = (data['username'],)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        # 判断账户状态
        if result[0][6] == 0:
            return jsonify({'success': False, 'message': '该账号已被封禁'})
        if result[0][6] == 2:
            return jsonify({'success': False, 'message': '该账号已被注销'})
        # 将用户输入的密码转换为字节串
        user_password_bytes = data['password'].encode('utf-8')
        # 将数据库中的密码转换为字节串
        hashed_passowrd = result[0][2].encode('utf-8')
        # 使用 checkpw() 函数比较哈希值和用户输入的密码
        is_password_match = bcrypt.checkpw(
            user_password_bytes, hashed_passowrd)
        if is_password_match:
            # 生成accesstoken
            access = f'${result[0][3]}${result[0][0]}'
            token = bcrypt.hashpw(access.encode('utf-8'), bcrypt.gensalt())
            accesstoken = access + token.decode('utf-8')
            # print(accesstoken)
            # 将该用户原有的token删除
            sql = "DELETE FROM `access_token` WHERE `user_id` = ?"
            val = (result[0][0])
            lock.acquire()
            dbcursor.execute(sql, val)
            lock.release()
            db.commit()
            # 将accesstoken存入数据库
            sql = "INSERT INTO `access_token` (`user_id`, `token`) VALUES (?, ?)"
            val = (result[0][0], accesstoken)
            lock.acquire()
            dbcursor.execute(sql, val)
            lock.release()
            db.commit()
            response = make_response(
                jsonify({'success': True, 'message': '登录成功'}))
            response.set_cookie('access-token', accesstoken, domain=DOMAIN,
                                max_age=15*24*3600, httponly=True)
            return response
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码不正确'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # print(data)
    sql = "SELECT * FROM `users` WHERE username = ?"
    val = (data['username'],)
    lock.acquire()
    dbcursor.execute(sql, val)
    lock.release()
    result = dbcursor.fetchall()
    # 判断该用户名是否存在
    if len(result) > 0:
        return jsonify({'success': False, 'message': '注册失败\n用户名已存在'})
    else:
        # 进行用户名密码的合法化判断
        if not check_username(data['username']):
            return jsonify({'success': False, 'message': '注册失败\n用户名不合法'})
        if not check_password(data['password']):
            return jsonify({'success': False, 'message': '注册失败\n密码不合法'})
        if data['password'] != data['repassword']:
            return jsonify({'success': False, 'message': '注册失败\n两次输入密码不一致'})
        # 对用户的密码进行加密存储
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO `users` (`username`, `password`, `nickname`) VALUES (?, ?, ?)"
        val = (data['username'], hashed_password, data['username'])
        lock.acquire()
        dbcursor.execute(sql, val)
        lock.release()
        db.commit()
        return jsonify({'success': True, 'message': '注册成功'})

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
            'tags': tags,
            'tagids': tagids,
            'language': language,
            'starnum': result[i][6],
            'updatetime': updatetime
        }
        # print(project)
        projectlist.append(project)

    return jsonify({'success': True, 'data': projectlist})

@app.route('/kinds', methods=['GET'])
def kinds():
    sql = "SELECT * FROM `kinds`"
    lock.acquire()
    dbcursor.execute(sql)
    lock.release()
    kinds = dbcursor.fetchall()
    kindlist = []
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
    
    return jsonify({'success': True, 'data': kindlist})

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
    
    return jsonify({'success': True, 'data': languagelist})

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
    
    return jsonify({'success': True, 'data': taglist})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)