from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)
from ..models.user import User

main = Blueprint('session', __name__)


@main.route("/", methods=['GET'])
def index():
    return redirect(url_for("blog.index"))


# 三大基本功能: 登陆 注销 注册
@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("user/login.html")
    user = User.validate_login(request.form)
    if user:
        # 设置session
        session["user_id"] = user.id
    else:
        return "用户不存在!"
    return redirect(url_for("blog.index"))


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("user/register.html")
    user = User.register(request.form)
    if user:
        # 设置session
        session["user_id"] = user.id
    else:
        return "Error: 用户名长度太短! or 用户名已存在! "
    return redirect(url_for("blog.index"))


@main.route("/logout", methods=['POST'])
def log_out():
    # 删除session
    session.pop("user_id")
    return redirect(url_for("blog.index"))


# 进阶功能: 找回密码
@main.route("/find", methods=['GET', 'POST'], endpoint="find")
def find_pwd():
    return "进阶功能: 找回密码(开发中)"


