from ._base import db, session

import os
import glob
import importlib


def register_modules(app):
    now_path = os.path.dirname(__file__) + os.sep
    now_path_size = len(now_path)
    for module in glob.glob(os.path.join(now_path, "**/[!_]*.py"), recursive=True):
        importlib.import_module("mvc.modules." + module[now_path_size:-3])
    db.init_app(app)
