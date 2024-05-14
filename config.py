import os
from dotenv import load_dotenv
load_dotenv(".flaskenv")

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
