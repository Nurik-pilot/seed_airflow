"""
Default configuration for the Airflow webserver
"""
from logging import getLogger
from os import environ
from pathlib import Path

from flask import current_app
from flask_appbuilder.security.manager import (
    AUTH_DB,
)

logger = getLogger(name=__name__)

current = Path(__file__)
basedir = current.parent.resolve()

WTF_CSRF_ENABLED: bool = True

AUTH_TYPE: int = AUTH_DB

RATELIMIT_STORAGE_URI = environ.get('RATELIMIT_STORAGE_URI')


@current_app.before_request
def print_custom_message() -> None:
    logger.info(
        msg='Executing before every request',
    )
