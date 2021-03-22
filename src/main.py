from flask import Flask

from controllers import register_controllers
from views import register_views

app = Flask(__name__)

if __name__ == '__main__':
    register_controllers(app)
    register_views(app)

    app.run()
