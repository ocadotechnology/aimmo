"""Django settings for example_project project."""
import mimetypes
import os

from django.http import Http404
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
USE_TZ = True

TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-gb"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "aimmo/static")]

mimetypes.add_type("application/wasm", ".wasm", True)

SECRET_KEY = "not-a-secret"
ROOT_URLCONF = "urls"

WSGI_APPLICATION = "example_project.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

INSTALLED_APPS = [
    "game",
    "pipeline",
    "portal",
    "aimmo",
    "common",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_js_reverse",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "rest_framework",
    "sekizai",  # for javascript and css management
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
            ]
        },
    }
]

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

PIPELINE = {
    "SASS_ARGUMENTS": "--quiet",
    "COMPILERS": ("game.pipeline_compilers.LibSassCompiler",),
    "STYLESHEETS": {
        "css": {
            "source_filenames": (
                os.path.join(BASE_DIR, "static/portal/sass/bootstrap.scss"),
                os.path.join(BASE_DIR, "static/portal/sass/colorbox.scss"),
                os.path.join(BASE_DIR, "static/portal/sass/styles.scss"),
            ),
            "output_filename": "portal.css",
        },
        "popup": {
            "source_filenames": (os.path.join(BASE_DIR, "static/portal/sass/partials/_popup.scss"),),
            "output_filename": "popup.css",
        },
        "game-scss": {
            "source_filenames": (os.path.join(BASE_DIR, "static/game/sass/game.scss"),),
            "output_filename": "game.css",
        },
    },
    "CSS_COMPRESSOR": None,
}

STATICFILES_FINDERS = [
    "pipeline.finders.PipelineFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

# This is used in common to enable/disable the OneTrust cookie management script
COOKIE_MANAGEMENT_ENABLED = False

CLOUD_STORAGE_PREFIX = "https://storage.googleapis.com/codeforlife-assets/"
SITE_ID = 1


def get_game_url_base_and_path(game_id: int) -> str:
    api_client = ApiClient()
    api_instance = CustomObjectsApi(api_client)
    result = api_instance.list_namespaced_custom_object(
        group="agones.dev", version="v1", namespace="default", plural="gameservers", label_selector=f"game-id={game_id}"
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
        return (f"http://{game_server_status['address']}:{game_server_status['ports'][0]['port']}", "/socket.io")
    except (KeyError, IndexError):
        raise Http404


AIMMO_GAME_SERVER_URL_FUNCTION = get_game_url_base_and_path
AIMMO_GAME_SERVER_SSL_FLAG = False

try:
    from example_project.local_settings import *  # pylint: disable=E0611
except ImportError:
    pass

from common.csp_config import *
