import logging
import os
from urllib.parse import quote_plus


class BaseConfig:
    # JSON配置
    JSON_AS_ASCII = False

    # 会话密钥配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'T-flask')

    # 默认日志等级
    LOG_LEVEL = logging.WARN

    # Mysql 配置
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME') or "root"
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or "123456"
    MYSQL_HOST = os.getenv('MYSQL_HOST') or "127.0.0.1"
    MYSQL_PORT = int(os.getenv('MYSQL_PORT') or 3308)
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or "demo"

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """ 测试配置 """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # 内存数据库


class DevelopmentConfig(BaseConfig):
    """ 开发配置 """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    """生成环境配置"""
    LOG_LEVEL = logging.ERROR

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 8


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
