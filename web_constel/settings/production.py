from .base import *
import django_heroku


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['constel.herokuapp.com', ]

CONTWE2_TOKEN = "zi3AvF41SP7MUBMkUw8Z"
CONTWE2_URL = 'wss://contwe2.herokuapp.com/ws/'

django_heroku.settings(locals())
