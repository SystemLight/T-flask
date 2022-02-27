import os
from typing import Literal, Optional

from flask import Flask

from .configs import config
from .extensions import init_plugs
from .view import init_view
from .scripts import init_scripts


def create_app(config_name: Optional[Literal['development', 'testing', 'production']] = None):
    app = Flask(os.getcwd())

    # 尝试从本地环境中读取
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])

    init_plugs(app)
    init_view(app)
    init_scripts(app)

    return app
