from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from ..models.todo import Todo
from blog_system.utils import log
from ..utils.login_required import login_required, current_user

main = Blueprint('todo', __name__)


@main.route('/')
@login_required
def index():
    # 查找当前登陆用户
    now_user = current_user()
    # 查找登陆用户的所有的todo 并返回
    todo_list = Todo.find_all(author_id=now_user.id)
    return render_template('todo/todo_index.html', todos=todo_list, now_user=now_user)


@main.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'GET':
        return redirect(url_for('.index'))
    form = request.form
    t = Todo.new(form)
    t.save()
    return redirect(url_for('.index'))


# 动态路由
@main.route('/delete/<int:todo_id>/', methods=["GET"])
@login_required
def delete(todo_id):
    # 查找当前登陆用户
    now_user = current_user()
    # 通过 id 删除todo
    if Todo.find(id=todo_id).author_id == now_user.id:
        Todo.delete(todo_id)
        log("deleted todo id: ", todo_id)
    return redirect(url_for('.index'))


# 更新todo
@main.route("/update", methods=["POST"])
def update():
    pass

