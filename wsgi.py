from flask_migrate import Migrate

from applications import create_app
from applications.extensions import db

app = create_app('testing')
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
