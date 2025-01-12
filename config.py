import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'AWS_EC2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app//static')
    TEMPLATE_FOLDER_APPLICATION = os.path.join(basedir, 'app//application//templates')
    TEMPLATE_FOLDER_COURSE = os.path.join(basedir, 'app//course//templates')
    TEMPLATE_FOLDER_ERRORS = os.path.join(basedir, 'app//errors//templates')
    TEMPLATE_FOLDER_USER = os.path.join(basedir, 'app//user//templates')

    # Microsoft Authentication Configurations
    AUTHORITY = os.getenv("AUTHORITY")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_PATH = "/getAToken" 
    ENDPOINT = 'ENDPOINT'
    SCOPE = ["User.Read"]

    SESSION_TYPE = "filesystem"
