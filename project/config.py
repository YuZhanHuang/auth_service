import logging
import os
from datetime import timedelta


class Config:
    # Basic settings
    PROJECT_ID = os.environ.get('PROJECT_ID')
    LOG_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get('SECRET_KEY', '5566neverdie')
    CORS_HEADERS = "Content-Type"

    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ['headers', 'query_string']
    JWT_ACCESS_COOKIE_PATH = '/jwt-tokens/access'
    JWT_REFRESH_COOKIE_PATH = '/jwt-tokens/refresh'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)

    # SMTP settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

    # database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{username}:{password}@{host}/{database_name}".format(
        username=os.environ.get('DB_USER', 'unicorn_user'),
        password=os.environ.get('DB_PASS', 'magical_password'),
        host=os.environ.get('DB_HOST', 'postgres'),
        database_name=os.environ.get('DB_NAME', 'postgres'),
    )

    # extension
    ALLOWED_EXTENSIONS = {"txt", "csv", "pdf", "png", "jpg", "jpeg", "gif", "zip"}


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'my secret'


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
