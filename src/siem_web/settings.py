"""
Django settings for siem_web project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y95dqs9x@+*8=bmjgdkod#usz1niw!t60l!k7x@x1ad^4bordr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'siemunlam.pythonanywhere.com']

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# Custom apps
	'accounts',
	'analytics',
	'auxilios',
	'medicos',
	'rules',

	# Third party apps
	'crispy_forms',
	'debug_toolbar',
	'rest_framework'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

	# Third party middleWare
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'siem_web.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [(os.path.join(BASE_DIR, "cross_app_templates"))],
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

WSGI_APPLICATION = 'siem_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		'ATOMIC_REQUESTS': True # Wraps each view in an atomic transaction
	}
}
"""   ON PRODUCTION  UNCOMMENT THIS
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': '',
		'USER': '',
		'PASSWORD': '',
		'HOST': '',    # Or an IP Address that your DB is hosted on
		'PORT': '', # default
	}
}"""

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")
	STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static-only")
	STATICFILES_DIRS = (
		os.path.join(os.path.dirname(BASE_DIR), "static", "static"),
	)

# Crispy-forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django-debug-toolbar settings
INTERNAL_IPS = ['127.0.0.1', 'localhost',]

# Django Rest Framework settings
REST_FRAMEWORK = {
    'PAGE_SIZE': 15,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # ON PRODUCTION USE: 'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    )
}

# JSON Web Token Authentication settings
JWT_AUTH = {
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

	'JWT_VERIFY_EXPIRATION': False,
	'JWT_EXPIRATION_DELTA': timedelta(seconds=1800),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=15),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}

# Authentication settings
LOGIN_URL = '/login/'

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#Django check --deploy
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False # used for HTTPS
SESSION_COOKIE_SECURE = False # used for HTTPS
CSRF_COOKIE_SECURE = False # used for HTTPS
CSRF_COOKIE_HTTPONLY = False


# Cross-app custom settings
AWS_BASE_URL = 'http://ec2-54-233-80-23.sa-east-1.compute.amazonaws.com:8085/serviciosSoporte'
CODE_AUXILIO_CANCELADO = 25
FIREBASE_AUTHORIZATION_KEY = 'AAAACZOgn48:APA91bGC3G0xrAbVpOHAIx8zYnhk5fcIGahsgnfx-4fU5-IDGghNrSH0viM5JV2jjLL3PakaDPU5jlMvrKw9Mq9BkfQANGsI0f6weSXuDoDPc32qNQzzYhc-gBYtJy8KKzITU5mCPW6o'
WS_CATEGORIZAR = AWS_BASE_URL + '/obtenerCategoria'
WS_REGLAS = AWS_BASE_URL + '/actualizarReglas'