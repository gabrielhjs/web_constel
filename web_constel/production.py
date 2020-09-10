from .base import *
import django_heroku


SECRET_KEY = os.environ.get('SECRET_KEY')

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = bool(os.environ.get('DEBUG_VALUE', False))

ALLOWED_HOSTS = ['constel.herokuapp.com']

CONTWE2_TOKEN = os.environ.get('CONTWE2_TOKEN')
CONTWE2_URL = os.environ.get('CONTWE2_URL')

django_heroku.settings(locals())
