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
