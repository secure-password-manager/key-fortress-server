from .base import *

ALLOWED_HOSTS = ['.key-fortress.com']

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    'https://key-fortress.com',
    "https://www.key-fortress.com"
]

CSRF_TRUSTED_ORIGINS = [
    'https://key-fortress.com',
    "https://www.key-fortress.com"
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_DOMAIN = 'key-fortress.com'
CSRF_COOKIE_DOMAIN = '.key-fortress.com'
