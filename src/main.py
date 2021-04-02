from flask import Flask

from mvc import use_mvc

app: Flask = use_mvc(Flask(__name__))
app.secret_key = "SystemLight"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa(path):
    """

    SPA单页应用路由

    :param path:
    :return:

    """
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run()
