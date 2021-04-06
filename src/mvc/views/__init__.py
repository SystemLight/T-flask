import os
import glob
import importlib


def register_views(app):
    now_path = os.path.dirname(__file__) + os.sep
    now_path_size = len(now_path)
    for module in glob.glob(os.path.join(now_path, "**/[!_]*.py"), recursive=True):
        app.register_blueprint(
            importlib.import_module("mvc.views." + module[now_path_size:-3]).blue_print
        )
