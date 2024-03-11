"""
Default configuration for the Airflow webserver
"""
from os import path

from flask_appbuilder.security.manager import (
    AUTH_DB,
)

basedir = path.abspath(
    path.dirname(__file__),
)

WTF_CSRF_ENABLED: bool = True

AUTH_TYPE: int = AUTH_DB
