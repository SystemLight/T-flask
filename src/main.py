from flask import Flask

from mvc import use_mvc

app: Flask = Flask(__name__)
app.secret_key = "SystemLight"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
use_mvc(app)


@app.errorhandler(400)
def bad_request(e):
    data = getattr(e, "data", None)
    if data:
        return {"data": data, "code": e.code}
    return e


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
