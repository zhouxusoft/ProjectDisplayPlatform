import re
import random

# 判断字符串中是否包含空白符
def has_white_space(s):
    return bool(re.search(r'\s', s))

# 判断用户名是否合法
def check_username(username):
    return bool(re.search(r'^(.{1,12})$', username) and not has_white_space(username))

# 判断密码是否合法
def check_password(password):
    return bool(re.search(r'^(.{6,20})$', password) and not has_white_space(password))

# 返回一个随机颜色的16进制 rgb 代码
def random_color():
    color = '{:06x}'.format(random.randint(0, 0xFFFFFF))
    return color