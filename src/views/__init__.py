from .hello import hello_views


def register_views(app):
    app.register_blueprint(hello_views)
