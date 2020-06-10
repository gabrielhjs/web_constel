from ..base import *


SECRET_KEY = os.environ.get('SECRET_KEY', 'abc')

DEBUG = os.environ.get('DEBUG_VALUE', False)

ALLOWED_HOSTS = ['constel.herokuapp.com', ]

CONTWE2_TOKEN = os.environ.get('CONTWE2_TOKEN')
CONTWE2_URL = os.environ.get('CONTWE2_URL')

django_heroku.settings(locals())