"""
Production settings for Render deployment.

This file imports everything from the base settings module, then overrides
the values that must differ in production (security, database, static/media
file handling, etc.).
"""

from .settings import *          # noqa: F401,F403  — inherit ALL base settings
import dj_database_url

# ---------------------------------------------------------------------------
# Core security
# ---------------------------------------------------------------------------
SECRET_KEY = config('SECRET_KEY')          # MUST be set in Render env vars
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.onrender.com').split(',')
CSRF_TRUSTED_ORIGINS = [
    f'https://{host.strip()}' for host in ALLOWED_HOSTS if host.strip()
]

# ---------------------------------------------------------------------------
# Database — Render provides a DATABASE_URL for the managed PostgreSQL
# ---------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=''),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ---------------------------------------------------------------------------
# Static files — served by WhiteNoise straight from the container
# ---------------------------------------------------------------------------
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')   # right after SecurityMiddleware
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ---------------------------------------------------------------------------
# Media files — Cloudinary (free tier: 25 GB storage, 25 GB bandwidth/month)
# Set CLOUDINARY_URL in Render env vars (format: cloudinary://API_KEY:API_SECRET@CLOUD_NAME)
# ---------------------------------------------------------------------------
INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']   # noqa: F405

STORAGES['default'] = {
    'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
}

# Keep MEDIA_URL so Django template {{ file.url }} still works
MEDIA_URL = '/media/'

# ---------------------------------------------------------------------------
# HTTPS / cookie hardening (Render terminates TLS at its proxy)
# ---------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# Logging — print everything to stdout so Render can capture it
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
