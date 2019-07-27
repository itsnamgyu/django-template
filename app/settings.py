"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.1.

Extended by Namgyu Ho as a custom django project template at
github.com/itsnamgyu/django-template
"""

import os

from django.core.exceptions import ImproperlyConfigured
from app.env_loader import require_env, fetch_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Variable to differentiate between development, staging, production etc.
# Consider changing <APP> to the name of your project. You MUST apply the
# same changes in wsgi.py
DJANGO_ENV = fetch_env('DJANGO_APP_ENV', default='DEV')

if DJANGO_ENV == 'DEV':
    DEBUG = True
    ALLOWED_HOSTS = ['*']
else:
    # Consider changing these for "real" production when your project get bigger
    DEBUG = True
    ALLOWED_HOSTS = ['*']

SECRET_KEY = require_env('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap4',
    'base',
    # default feature apps
    'blurb',
    # additional feature apps (uncomment to enable)
    'modern_email',
    'django_stripe',
    # example app w/ index page for testing
    'example',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    # 'social_core.backends.google.GoogleOAuth2',  # uncomment for Google signin
    # 'social_core.backends.facebook.FacebookOAuth2',  # uncomment for Facebook signin
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# The following settings pertain to django-allauth
"""
Allauth requires some manual setup on your part. Make sure to have a good
understanding of the basics and the setup process before you start. You can
read more here:
https://django-allauth.readthedocs.io/en/latest/installation.html
"""

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True

SITE_ID = 1

# Uncomment for social login
"""
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_URL_NAMESPACE = 'social'
"""

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = require_env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = require_env('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = 'us-west-2'  # default is us-east-1
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'  # default is us-east-1

MODERN_EMAIL_STATIC_HOST = 'http://stage.gyu.io/'
MODERN_EMAIL_LOGO_IMAGE = 'img/logo.png'
MODERN_EMAIL_CUSTOM_TEMPLATE = None
MODERN_EMAIL_SUPPORT_EMAIL = 'support@gyu.io'
MODERN_EMAIL_ADDRESS_LINE_1 = 'Address Line 1'
MODERN_EMAIL_ADDRESS_LINE_2 = 'Address Line 2'
MODERN_EMAIL_ORGANIZATION_NAME = 'My Site'
MODERN_EMAIL_COPYRIGHT_START_YEAR = '2019'

STRIPE_PUBLIC_KEY = require_env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = require_env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SIGNING_SECRET = require_env('STRIPE_WEBHOOK_SIGNING_SECRET')
STRIPE_SUPPORT_EMAIL = 'support@gyu.io'
