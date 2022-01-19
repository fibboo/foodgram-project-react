import os

import environ

from . import BASE_DIR, env, DEBUG

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env(
            'DB_ENGINE', default='django.db.backends.postgresql'
        ),
        'NAME': env('DB_NAME', default='foodgram'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='password'),
        'HOST': env('DB_HOST', default='db'),
        'PORT': env('DB_PORT', default='5432')
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = 'api/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
