import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'you_know_right'

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
