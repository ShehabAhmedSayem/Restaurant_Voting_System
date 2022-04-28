import socket
from .default import *
from .default import env

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
        'OPTIONS': {
            'sslmode': env.str('DB_SSLMODE'),
        },
    }
}

DEFAULT_FROM_EMAIL = ''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

CORS_ALLOW_ALL_ORIGINS = True

# DEBUG TOOLBAR
INTERNAL_IPS = ['127.0.0.1']

# If Docker is used then uncomment this to get internal ip
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = (
    [ip[: ip.rfind(".")] + ".1" for ip in ips]
    + ["127.0.0.1", "10.0.2.2"]
)
