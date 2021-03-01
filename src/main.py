from flask import Flask

from views.hello import hello_blueprint

if __name__ == '__main__':
    app = Flask(__name__)

    app.register_blueprint(hello_blueprint)

    app.run()
