"""Изолированные проверки основы. Не настройка демонстрационного сервера."""
import os
import secrets

os.environ.setdefault("DJANGO_SECRET_KEY", secrets.token_urlsafe(48))
os.environ.setdefault("DB_PASSWORD", secrets.token_urlsafe(32))

from .settings import *  # noqa: E402,F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
ALLOWED_HOSTS = ["testserver", "127.0.0.1", "localhost"]
