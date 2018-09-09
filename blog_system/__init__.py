# encoding: utf-8
# __author__ = "wyb"
# date: 2018/9/9
from flask import Flask

from .routes.user import main as user_route
from .routes.blog import main as blog_route
from .routes.todo import main as todo_route


app = Flask(__name__)
app.secret_key = 'test for good'


# 注册蓝图
app.register_blueprint(user_route)                                 # 基础路由: 登陆注册注销
app.register_blueprint(blog_route, url_prefix='/blog')             # 博客路由
app.register_blueprint(todo_route, url_prefix='/todo')             # todo路由


