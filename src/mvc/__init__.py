from .controllers import register_controllers
from .views import register_views


def use_mvc(app):
    register_controllers(app)
    register_views(app)

    return app
