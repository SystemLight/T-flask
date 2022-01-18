from ..context import app


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def default__catch_all(path):
    return app.send_static_file("index.html")
