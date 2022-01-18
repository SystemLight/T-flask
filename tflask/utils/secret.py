from itsdangerous import TimedJSONWebSignatureSerializer

from ..context import app

jwt = TimedJSONWebSignatureSerializer(secret_key=app.config["SECRET_KEY"], expires_in=2592000)
