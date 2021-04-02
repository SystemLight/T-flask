from .api import api_controller


def register_controllers(app):
    app.register_blueprint(api_controller)
