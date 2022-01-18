from .context import app

app.config["SECRET_KEY"] = "SystemLight"

app.config["JSON_AS_ASCII"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
