from flask import render_template

from ._base import bp
from . import home


def init_app(app):
    app.register_blueprint(bp)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa_route(path):
        """

        SPA单页应用路由

        :param path:
        :return:

        """
        return app.send_static_file("index.html")

    @app.route("/home", methods=["GET"])
    def home_route():
        return render_template("home.html")
