from .modules import register_modules
from .views import register_views
from .controllers import register_controllers


def use_mvc(app, need_migrate=False):
    register_modules(app, need_migrate)
    register_views(app)
    register_controllers(app)

    return app
