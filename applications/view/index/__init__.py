from .index import index_bp


def register_index_views(app):
    app.register_blueprint(index_bp)
