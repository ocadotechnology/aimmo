# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2015, Ocado Innovation Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.
"""Django settings for example_project project."""
import os
import mimetypes

from django.http import Http404
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from aimmo_runner.minikube import get_ip

ALLOWED_HOSTS = ["*"]

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Add 'postgresql_psycopg2', 'mysql',
        # 'sqlite3' or 'oracle'.
        "NAME": os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.sqlite3"),
        # Or path to database file if using sqlite3.
    }
}

USE_I18N = True
USE_L10N = True

TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-gb"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")
STATIC_URL = "/static/"
SECRET_KEY = "not-a-secret"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

mimetypes.add_type("application/wasm", ".wasm", True)

ROOT_URLCONF = "example_project.urls"

WSGI_APPLICATION = "example_project.wsgi.application"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "portal",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {"views": {"handlers": ["console"], "level": "DEBUG"}},
}

LOGIN_URL = "/kurono/accounts/login/"

LOGIN_REDIRECT_URL = "/kurono/"

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# This is used in common to enable/disable the OneTrust cookie management script
COOKIE_MANAGEMENT_ENABLED = False


def get_base_url_for_game():
    return f"http://{get_ip()}:8000"


def get_game_url_base_and_path(game_id: int) -> str:
    api_client = ApiClient()
    api_instance = CustomObjectsApi(api_client)
    result = api_instance.list_namespaced_custom_object(
        group="agones.dev",
        version="v1",
        namespace="default",
        plural="gameservers",
        label_selector=f"game-id={game_id}",
    )
    try:
        result_items = result["items"]
        game_server = None

        # Get the first game server not marked for deletion. Raise 404 if there is none.
        for item in result_items:
            if "deletionTimestamp" not in item["metadata"]:
                game_server = item
                break

        if game_server is None:
            raise Http404

        game_server_status = game_server["status"]
        return (
            f"http://{game_server_status['address']}:{game_server_status['ports'][0]['port']}",
            "/socket.io",
        )
    except (KeyError, IndexError):
        raise Http404


AIMMO_GAME_SERVER_URL_FUNCTION = get_game_url_base_and_path
AIMMO_GAME_SERVER_SSL_FLAG = False
AIMMO_DJANGO_BASE_URL = get_base_url_for_game()

try:
    from example_project.local_settings import *  # pylint: disable=E0611
except ImportError:
    pass


from django_autoconfig import autoconfig

autoconfig.configure_settings(globals())
