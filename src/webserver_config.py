"""
Default configuration for the Airflow webserver
"""
from os import environ
from pathlib import Path

from flask_appbuilder.security.manager import (
    AUTH_DB,
)

current = Path(__file__)
basedir = current.parent.resolve()

WTF_CSRF_ENABLED: bool = True

AUTH_TYPE: int = AUTH_DB

RATELIMIT_STORAGE_URI = environ.get('RATELIMIT_STORAGE_URI')
