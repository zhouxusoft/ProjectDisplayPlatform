import re
def has_white_space(s):
    return bool(re.search(r'\s', s))

def check_username(username):
    return bool(re.search(r'^(.{1,12})$', username) and not has_white_space(username))

def check_password(password):
    return bool(re.search(r'^(.{6,20})$', password) and not has_white_space(password))