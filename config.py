import configparser
import os
import random
import string

user = os.environ.get('DATABASE_USER')
passwd = os.environ.get('DATABASE_PASSWORD')
database = os.environ.get('DATABASE_NAME')
host = os.environ.get('DATABASE_HOST')
port = '5432'
gen = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(gen) for i in range(12))

SQLALCHEMY_DATABASE_URI = 'postgresql://'+user+':'+password+'@'+host+'/' + database
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = key
DEBUG = False
