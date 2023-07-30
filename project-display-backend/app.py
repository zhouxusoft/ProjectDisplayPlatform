from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# 允许所有的跨域请求
CORS(app)
# 自定义允许跨域的源
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1"}})



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)