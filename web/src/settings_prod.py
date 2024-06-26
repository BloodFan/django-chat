from .settings import *
from .settings import USE_HTTPS

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True  # change this for production

CSRF_TRUSTED_ORIGINS = [
    "https://dev.kimaykin-django.ru",
    "https://chat.dev.kimaykin-django.ru",
]

X_FRAME_OPTIONS = 'DENY'

# Only via HTTPS
if USE_HTTPS:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'strict-origin'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
