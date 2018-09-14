from ..models import Model
import hashlib


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @staticmethod
    def hashed_password(pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        user = User.find_by(username=name)
        # 返回给views的处理结果
        res = {
            "error": 0,
            "message": "",
            "user": ""
        }
        if not name:
            res["error"] = 1
            res["message"] = "用户名不能为空!"
            return res
        elif not pwd:
            res["error"] = 1
            res["message"] = "密码不能为空!"
            return res
        elif user is not None:
            res["error"] = 1
            res["message"] = "用户名已存在!"
            return res
        elif len(name) <= 2:
            res["error"] = 1
            res["message"] = "用户名不能少于三位!"
            return res
        elif len(pwd) <= 2:
            res["error"] = 1
            res["message"] = "密码不能少于三位!"
            return res
        else:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            res["message"] = "成功注册!"
            res["user"] = u
            return res

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        # todo 改写登陆验证 类似于注册和改密码那样写
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    @classmethod
    def change_pwd(cls, form):
        username = form.get("username")
        old_pwd = form.get("password")
        new_pwd = form.get("password2")
        user = User.find_by(username=username)
        # 返回给views的处理结果
        res = {
            "error": 0,
            "message": ""
        }

        if not username:
            res["error"] = 1
            res["message"] = "用户名不能为空!"
            return res
        elif not old_pwd:
            res["error"] = 1
            res["message"] = "旧密码不能为空!"
            return res
        elif not new_pwd:
            res["error"] = 1
            res["message"] = "新密码不能为空!"
            return res
        elif user is None:
            res["error"] = 1
            res["message"] = "用户名不存在!"
            return res
        elif user.password != User.salted_password(old_pwd):
            res["error"] = 1
            res["message"] = "旧密码错误!"
            return res
        elif old_pwd == new_pwd:
            res["error"] = 1
            res["message"] = "新密码不能和旧密码相同"
            return res
        else:
            user.password = User.salted_password(new_pwd)
            user.save()
            res["message"] = "修改密码成功!"
            return res
