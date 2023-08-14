from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from create_db import create_database
from modules import *
import pymysql
import bcrypt
import os

load_dotenv()
# 从配置文件中读取数据
MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST")
MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER")
MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD")
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN").split(",")
ALLOW_ORIGIN = [origin.strip() for origin in ALLOW_ORIGIN]

create_database()

# 数据库连接
db = pymysql.connect(
    host=MYSQL_DATABASE_HOST,
    user=MYSQL_DATABASE_USER,
    password=MYSQL_DATABASE_PASSWORD,
    db="project_display",
    charset="utf8mb4"
)
dbcursor = db.cursor()

app = Flask(__name__)

# 自定义允许跨域的源
CORS(app, resources={r"/*": {"origins": ALLOW_ORIGIN, "supports_credentials": True}})

# 在所有请求前判断数据库连接状态
@app.before_request
def before_request():
    if not db.open:
        db.connect()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    # 从用户表中查询用户， 并对密码作出判断
    sql = "SELECT * FROM `user_table` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
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
            sql = "DELETE FROM `access_token` WHERE `user_id` = %s"
            val = (result[0][0])
            dbcursor.execute(sql, val)
            db.commit()
            # 将accesstoken存入数据库
            sql = "INSERT INTO `access_token` (`user_id`, `token`) VALUES (%s, %s)"
            val = (result[0][0], accesstoken)
            dbcursor.execute(sql, val)
            db.commit()
            response = make_response(
                jsonify({'success': True, 'message': '登录成功'}))
            response.set_cookie('access-token', accesstoken,
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
    sql = "SELECT * FROM `user_table` WHERE username = %s"
    val = (data['username'],)
    dbcursor.execute(sql, val)
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
        sql = "INSERT INTO `user_table` (`username`, `password`, `nickname`) VALUES (%s, %s, %s)"
        val = (data['username'], hashed_password, data['username'])
        dbcursor.execute(sql, val)
        db.commit()
        return jsonify({'success': True, 'message': '注册成功'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)