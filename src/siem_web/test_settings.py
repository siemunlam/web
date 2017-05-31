from .settings import *

# SQLite3 on memory implementation
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# So it doesn't actually send emails
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'