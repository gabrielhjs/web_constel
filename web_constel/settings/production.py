from ..base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = ['constel.herokuapp.com', '0.0.0.0', 'localhost', '127.0.0.1']

CONTWE2_TOKEN = os.environ.get('CONTWE2_TOKEN')
CONTWE2_URL = os.environ.get('CONTWE2_URL')

django_heroku.settings(locals())
