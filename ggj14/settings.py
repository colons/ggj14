"""
Django settings for ggj14 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['ggj14.colons.co']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pipeline',

    'ggj14',
    'ggj14.apps.chat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ggj14.urls'

WSGI_APPLICATION = 'ggj14.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'interactions': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'interactions.log'),
        },
    },
    'loggers': {
        'interactions': {
            'handlers': ['interactions'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# PIPELINE

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = ('pipeline.compilers.less.LessCompiler',)

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_DISABLE_WRAPPER = True

PIPELINE_CSS = {
    'style': {
        'source_filenames': [
            'less/style.less',
        ],
        'output_filename': 'css/style.min.css',
    }
}

PIPELINE_JS = {
    'script': {
        'source_filenames': [
            'js/libs/jquery.js',
            'js/libs/handlebars.js',
            'js/csrf.js',
            'js/chat.js',
        ],
        'output_filename': 'js/min/script.js',
    },
}

# GGJ14

FOIL_NAME = 'Ymir'
CHANNEL_NAME = '#interboats'

from settings_local import *  # NOQA
