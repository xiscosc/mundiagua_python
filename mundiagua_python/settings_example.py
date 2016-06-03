from settings import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

BOWER_COMPONENTS_ROOT = '/Users/xiscosastre/PycharmProjects/mundiagua_python/components/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mundiagua_py',
        'USER': 'xiscosastre',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ESENDEX_USERNAME = 'yourusername'
ESENDEX_PASSWORD = 'mysecretpassword'
ESENDEX_ACCOUNT = 'account-key-provided-by-esendex'
ESENDEX_SANDBOX = False # True if yo like test first
SENDGRID_USER = "user"
SENDGRID_PASSWORD = "pass"

DEBUG = True
DOMAIN = "https://www.example.com"
ALLOWED_HOSTS = ['.example.com']