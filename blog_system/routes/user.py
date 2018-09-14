from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
    flash,
    get_flashed_messages,
)
from ..models.user import User

main = Blueprint('session', __name__)


@main.route("/", methods=['GET'])
def index():
    return redirect(url_for("blog.index"))


# 四大基本功能: 登陆 注销 注册 改密
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
        return "用户名已存在!"
    return redirect(url_for("blog.index"))


@main.route("/logout", methods=['POST'])
def log_out():
    # 删除session
    session.pop("user_id")
    return redirect(url_for("blog.index"))


# 进阶功能: 更改密码
@main.route("/changePwd", methods=['GET', 'POST'], endpoint="change")
def find_pwd():
    if request.method == "GET":
        # 取错误信息
        error_message = get_flashed_messages(category_filter=["changePwd_message"])
        if not error_message:
            error_message = ""
        else:
            error_message = "错误信息: " + error_message[0]
        return render_template("user/change-pwd.html", error_message=error_message)
    else:
        status = User.change_pwd(request.form)
        # 设置错误信息并重定向
        if status["error"]:
            flash(status["message"], category="changePwd_message")
            return redirect(url_for(".change"))
        return status["message"]


