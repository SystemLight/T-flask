import os

from dotenv import load_dotenv


def init_dotenv():
    flask_env_path = os.path.join(os.getcwd(), '.flaskenv')
    if os.path.exists(flask_env_path):
        load_dotenv(flask_env_path)
