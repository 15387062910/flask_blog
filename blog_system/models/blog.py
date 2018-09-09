import time
from ..models import Model
from ..models.user import User

# 针对我们的数据 comment
# 我们要做 4 件事情
"""
C create 创建数据
R read 读取数据
U update 更新数据
D delete 删除数据

Comment.new() 来创建一个 todo
"""


class Blog(Model):
    @classmethod
    def new(cls, form):
        """
        创建并保存一个对象并且返回它
        xxx.new({'title': '吃饭'})
        :param form: 一个字典
        :param user: 创建博客的用户
        :return: 创建的实例
        """
        # 下面一行相当于 t = xxx(form)
        t = cls(form)
        t.save()
        return t

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.create_time = int(time.time())
        self.author_id = int(form.get('author_id', 0))
        self.author_name = self.find_author()

    def find_author(self):
        author = User.find(id=self.author_id)
        if author:
            return author.username
        else:
            return ""


class BlogComment(Model):
    @classmethod
    def new(cls, form):
        """"
        创建并保存一个对象并且返回它
        xxx.new({'content': '666'})
        :param form: 一个字典
        :param user: 创建评论的用户
        :return: 创建的实例
        """
        # 下面一行相当于 t = xxx(form)
        t = cls(form)
        t.save()
        return t

    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.create_time = int(time.time())
        self.author_id = int(form.get('author_id', 0))
        self.blog_id = int(form.get('blog_id', 0))
        self.author_name = self.find_author()

    def find_author(self):
        author = User.find(id=self.author_id)
        if author:
            return author.username
        else:
            return ""


