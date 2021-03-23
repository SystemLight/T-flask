from flask import Flask

from controllers import register_controllers
from views import register_views

app = Flask(__name__)

app.secret_key = "SystemLight"

register_controllers(app)
register_views(app)

if __name__ == '__main__':
    app.run()
