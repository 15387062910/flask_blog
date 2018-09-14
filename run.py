from blog_system import app


# 运行代码
if __name__ == '__main__':
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=8000,
    )
    app.run(**config)
