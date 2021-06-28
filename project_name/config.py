SECRET_KEY = "SystemLight"
JSON_AS_ASCII = False
RESTFUL_JSON = {"ensure_ascii": JSON_AS_ASCII}

DATABASE_FILE = "foo.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FILE}"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

BABEL_DEFAULT_LOCALE = "zh-CN"

FLASK_ADMIN_SWATCH = "cerulean"
