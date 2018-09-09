# encoding: utf-8
# __author__ = "wyb"
# date: 2018/9/9
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)
from ..models.user import User
import functools


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


def login_required(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # 获得session对应值
        user = current_user()
        if user is None:
            # 登录页面
            return render_template("user/login.html")
        else:
            return func(*args, **kwargs)
    return inner




