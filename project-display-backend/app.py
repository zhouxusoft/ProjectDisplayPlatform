from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import bcrypt
import os

load_dotenv()

# 数据库连接
db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    db="fontlibrary",
    charset="utf8mb4"
)
dbcursor = db.cursor()

app = Flask(__name__)

# 自定义允许跨域的源
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173", "supports_credentials": True}})

# 在所有请求前判断数据库连接状态
@app.before_request
def before_request():
    if not db.open:
        db.connect()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    response = jsonify({'message': 'Login successful'})
    return response
    # 从用户表中查询用户， 并对密码作出判断
    # sql = "SELECT * FROM `usertable` WHERE username = %s"
    # val = (data['username'],)
    # dbcursor.execute(sql, val)
    # result = dbcursor.fetchall()
    # # 判断该用户名是否存在
    # if len(result) > 0:
    #     # 将用户输入的密码转换为字节串
    #     user_password_bytes = data['password'].encode('utf-8')
    #     # 将数据库中的密码转换为字节串
    #     hashed_passowrd = result[0][2].encode('utf-8')
    #     # 使用 checkpw() 函数比较哈希值和用户输入的密码
    #     is_password_match = bcrypt.checkpw(
    #         user_password_bytes, hashed_passowrd)
    #     if is_password_match:
    #         # 生成accesstoken
    #         access = f'${result[0][3]}${result[0][0]}'
    #         token = bcrypt.hashpw(access.encode('utf-8'), bcrypt.gensalt())
    #         accesstoken = access + token.decode('utf-8')
    #         # print(accesstoken)
    #         # 将该用户原有的token删除
    #         sql = "DELETE FROM `access-token` WHERE `userId` = %s"
    #         val = (result[0][0])
    #         dbcursor.execute(sql, val)
    #         db.commit()
    #         # 将accesstoken存入数据库
    #         sql = "INSERT INTO `access-token` (`userId`, `token`) VALUES (%s, %s)"
    #         val = (result[0][0], accesstoken)
    #         dbcursor.execute(sql, val)
    #         db.commit()
    #         response = make_response(
    #             jsonify({'success': True, 'message': '登录成功'}))
    #         response.set_cookie('access-token', accesstoken,
    #                             max_age=15*24*3600, httponly=True)
    #         return response
    #     else:
    #         return jsonify({'success': False, 'message': '用户名或密码不正确'})
    # else:
    #     return jsonify({'success': False, 'message': '用户名或密码不正确'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)