"""Django settings for example_project project."""
import os
import mimetypes

from django.http import Http404
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient

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

try:
    from example_project.local_settings import *  # pylint: disable=E0611
except ImportError:
    pass


from django_autoconfig import autoconfig

autoconfig.configure_settings(globals())
