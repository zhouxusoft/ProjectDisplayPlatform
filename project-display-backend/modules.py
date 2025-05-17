import re
import random
import datetime

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

def calculate_decay_factor(hours):
    """
    根据经过小时数计算时间衰减因子：
    - 衰减前50%时，使用0.5%每小时衰减（0.995^hours）
    - 衰减至50%以下后，使用0.1%每小时衰减（0.999^hours）
    """
    # 计算衰减到50%所需时间 t 满足 0.995^t = 0.5
    # t = log(0.5) / log(0.995)
    import math
    t = math.log(0.5) / math.log(0.995)

    if hours <= t:
        decay = 0.995 ** hours
    else:
        decay = 0.5 * (0.999 ** (hours - t))
    return decay

def calculate_score(likes, views, publish_time, current_time=None):
    """
    计算单个条目的综合得分。
    参数：likes: 点赞数，views: 浏览数，publish_time: 发布时间，datetime对象，current_time: 当前时间
    返回：综合得分（浮点数）
    """
    if current_time is None:
        current_time = datetime.now() # type: ignore
    # 计算时间差（小时）
    delta = current_time - publish_time
    hours = delta.total_seconds() / 3600
    # 计算时间衰减因子
    decay_factor = calculate_decay_factor(hours)
    # 计算热度权重
    hotness = likes * 5 + views
    # 综合得分
    score = hotness * decay_factor
    return score