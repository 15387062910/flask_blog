from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from ..models.blog import (
    Blog,
    BlogComment,
)
from ..utils.login_required import login_required, current_user

main = Blueprint('blog', __name__)


# 博客首页
@main.route("/", methods=["GET"])
def index():
    blogs = Blog.all()
    return render_template("blog/blog_index.html", blogs=blogs)


# 发布新博客页面
@main.route("/new", methods=["GET"])
@login_required
def new():
    user = current_user()
    return render_template("blog/blog_new.html", author=user)


# 添加新博客
@main.route("/add", methods=["POST"])
@login_required
def add():
    Blog.new(request.form)
    return redirect(url_for(".index"))


# /blog/1
@main.route("/<int:blog_id>", methods=["GET"])
def view(blog_id):
    blog = Blog.find(id=blog_id)
    comments = BlogComment.find_all(blog_id=blog_id)
    now_user = current_user()
    return render_template("blog/blog_detail.html", blog=blog, comments=comments, author=now_user)


# 添加评论
@main.route("/comment/new", methods=["POST"])
@login_required
def comment():
    form = request.form
    BlogComment.new(form)
    return redirect(url_for(".view", blog_id=form.get("blog_id")))


# 传统web： 传递回来一个页面
# 现代web： 是做成服务 访问一个网址，返回了json数据或其他数据
# 这样做的好处:
"""
    1. 不同服务，可以用不用的语言
    2. 拆分服务 业务里面 有一些部分很耗费性能，有一些部分不怎么耗费性能
    拆分服务:
        传统做法: 开n个app 对应不同的用户，让他访问不同的app
        每个服务独立(支付、普通功能等)，复制的单位，是以服务为基础的 微服务，SOA,面向服务的架构
"""



