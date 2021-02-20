from .base import *
import django_heroku


SECRET_KEY = os.environ.get('SECRET_KEY')

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = (os.environ.get('DEBUG_VALUE', 'False') == 'True')

ALLOWED_HOSTS = ['constel.herokuapp.com']

CONTWE2_TOKEN = os.environ.get('CONTWE2_TOKEN')
CONTWE2_URL = os.environ.get('CONTWE2_URL')
SENTINELA_WE = os.environ.get('SENTINELA_WE')

django_heroku.settings(locals())
