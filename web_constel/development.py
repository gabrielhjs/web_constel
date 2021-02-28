from .base import *

SECRET_KEY = 'n+u8xajvvog6g!9rja3eqsak$@n5k2or=%+&)rbvr$j&x3weg@'

DEBUG = True

ALLOWED_HOSTS = []

CONTWE2_TOKEN = "zi3AvF41SP7MUBMkUw8Z"
CONTWE2_URL = "wss://contwe2.herokuapp.com/ws/"
SENTINELA_WE = "ws://127.0.0.1:5000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teste',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# CONTWE2_TOKEN = "abc"
# CONTWE2_URL = 'ws://127.0.0.1:8080/ws/'
