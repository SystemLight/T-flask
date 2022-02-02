from .index import register_index_views


def init_view(app):
    register_index_views(app)
