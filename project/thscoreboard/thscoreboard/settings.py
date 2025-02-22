"""
Django settings for thscoreboard project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
IS_HEROKU = "DYNO" in os.environ
IS_PROD = IS_HEROKU
if not IS_PROD:
    import dotenv
    dotenv.load_dotenv()

from pathlib import Path

from django.utils.translation import gettext_lazy as _


def GetBooleanFromEnvironment(key, default):
    if key not in os.environ:
        return default
    elif os.environ[key].lower() == 'true':
        return True
    elif os.environ[key].lower() == 'false':
        return False
    else:
        value = os.environ[key]
        raise EnvironmentError(f'Environment variable for key {key} was {value}, not true or false.')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

if IS_PROD:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    SECRET_KEY = 'django-insecure-satv#@fo8oe#=$hip@6w7qaktz0=!$b@2dtev+x(8ne*_7e2ic'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PROD

# Whether or not to require a passcode to sign up for the site.
REQUIRE_PASSCODE = GetBooleanFromEnvironment('REQUIRE_PASSCODE', True)


def _GetAllowedHosts():
    hosts = ['localhost', 'local.silentselene.net']
    env_host = os.environ.get('MY_HOST')
    if env_host:
        hosts.append(env_host)
    return hosts


ALLOWED_HOSTS = _GetAllowedHosts()
print('Allowed hosts: {}'.format(', '.join(ALLOWED_HOSTS)))

SITE_BASE = os.environ.get("SITE_BASE")
if not SITE_BASE:
    SITE_BASE = "http://localhost:8000"

CSRF_TRUSTED_ORIGINS = [SITE_BASE]

# Application definition

DEV_ONLY_APPS = ['rosetta']

INSTALLED_APPS = [
    'shared_content.apps.SharedContentConfig',
    'replays.apps.ReplaysConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'django.contrib.humanize'
] + (DEV_ONLY_APPS if DEBUG else [])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.record_ip.RecordIPMiddleware',
    'users.middleware.check_ban.CheckBanMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thscoreboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['thscoreboard/templates/'],
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

WSGI_APPLICATION = 'thscoreboard.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # This logger will log all SQL queries. It is useful when debugging.
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        # },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if 'DATABASE_SOCKET' in os.environ:
    # We are on a server that only accepts database connections on a socket
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('LOCAL_DATABASE_NAME', 'thscoreboard'),
            'USER': os.environ.get('LOCAL_DATABASE_USER', 'thscoreboard'),
            'PASSWORD': os.environ['LOCAL_DATABASE_PASSWORD'],
        },
    }
else:
    # Use local database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('LOCAL_DATABASE_NAME', 'thscoreboard'),
            'HOST': 'localhost',
            'PORT': '5432',
            'USER': os.environ.get('LOCAL_DATABASE_USER', 'thscoreboard'),
            'PASSWORD': os.environ['LOCAL_DATABASE_PASSWORD'],
        },
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', _('English')),
    ('ja', _('Japanese')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATE_FORMAT = '%Y-%m-%d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

SASS_PROCESSOR_ROOT = 'compiled_static_css/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/users/login'

LOGIN_REDIRECT_URL = '/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

if os.environ.get('EMAIL_HOST'):
    print('Using production SMTP!')
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ['EMAIL_HOST']
    print(f'SMTP host: {EMAIL_HOST}')
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = 'no-reply@silentselene.net'
else:
    print('Using DEVELOPER CONSOLE SMTP; no real emails will be sent!')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DISCORD_WEBHOOK_ID = os.environ.get('DISCORD_WEBHOOK_ID', None)
DISCORD_WEBHOOK_TOKEN = os.environ.get('DISCORD_WEBHOOK_TOKEN', None)
