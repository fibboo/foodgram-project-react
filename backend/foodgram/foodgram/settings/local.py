# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
import os

from . import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')
MEDIA_URL = '/media/'
