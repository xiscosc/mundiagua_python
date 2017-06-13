"""
Django settings for mundiagua_python project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jn$^4^oa*&k6ssdxz5ff^d8w#7(_u46olig8t97qd0!sic0&nh'



# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OTHER_APPS = [
    'colorfield',
    'djangobower',
    'bootstrapform',
    'bootstrap_pagination',
    'async_messages',
    'hijack',
    'compat',
    'hijack_admin',
    'admin_honeypot',
    'easy_thumbnails',
]

MY_APPS = [
    'core',
    'client',
    'intervention',
    'budget',
    'repair',
    'engine',
]


INSTALLED_APPS = DJANGO_APPS + OTHER_APPS + MY_APPS

BOWER_INSTALLED_APPS = (
    'https://github.com/BlackrockDigital/startbootstrap-sb-admin-2.git',
    'material-avatar',
    'bootstrap3-typeahead',
    'metisMenu',
    'remarkable-bootstrap-notify',
    'animate.css'
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'async_messages.middleware.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.login.EnforceLoginMiddleware',
    'core.middleware.staff.StaffMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

PUBLIC_URLS = (
    r'login/',
    r'login/google/',
    r'login/google/process/',
    r'login/google/error/',
    r'logout/',
    r'admin/',
    r'repair-status/(?P<online>\w+)/',
    r'clientes/'
)

ROOT_URLCONF = 'mundiagua_python.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mundiagua_python.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

ASSIGNED_STATUS = 2

AUTH_USER_MODEL = 'core.User'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.request",
            ],
        },
    },
]


MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

DEFAULT_NUM_PAGINATOR = 5
DEFAULT_BUDGETS_PAGINATOR = 7
DEFAULT_CLIENTS_PAGINATOR = 18
DEFAULT_MODIFICATIONS_PAGINATOR = 18

EMAIL_BACKEND = "sgbackend.SendGridBackend"

LOGIN_URL = "/login/"

HIJACK_REGISTER_ADMIN = False
HIJACK_ALLOW_GET_REQUESTS = True
HIJACK_USE_BOOTSTRAP = True
HIJACK_LOGIN_REDIRECT_URL = '/'  # Where admins are redirected to after hijacking a user
HIJACK_LOGOUT_REDIRECT_URL = '/spectrum/core/user/'  # Where admins are redirected to after releasing a user


CELERY_RESULT_BACKEND = 'cache+memcached://127.0.0.1:11211/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

NON_STAFF_VIEWS = ('message-new',
                   'message-inbox',
                   'message-sent',
                   'message-ajax',
                   'intervention-list-own',
                   'intervention-view',
                   'intervention-forbidden',
                   'client-address-edit-geo',
                   'home',
                   'logout',
                   'login',
                   'login-google',
                   'release_hijack',
                   'intervention-image-upload',
                   'intervention-status-job',
                   'changelog',
                   'user-manage',
                   'password-change',
                   'password-change-done')

THUMBNAIL_ALIASES = {
    '': {
        'intervention_th': {'size': (100, 100), 'crop': True},
    },
}

MEDIA_URL = "/media/"

SESSION_COOKIE_AGE = 60 * 60 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

APP_VERSION = "6.3alpha"

LOGIN_REDIRECT_URL = "/"
