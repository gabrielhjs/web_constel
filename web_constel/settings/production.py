from .base import *
import django_heroku


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG_VALUE', False)

ALLOWED_HOSTS = ['constel.herokuapp.com', ]

CONTWE2_TOKEN = os.environ.get('CONTWE2_TOKEN')
CONTWE2_URL = os.environ.get('CONTWE2_URL')

DATABASE_URL = os.environ.get('DATABASE_URL')

django_heroku.settings(locals())
