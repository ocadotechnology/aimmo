import os

dirname = os.path.dirname
abspath = os.path.abspath

db_name = os.path.join(abspath(dirname(dirname(abspath(__file__)))), "db.sqlite3")

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": db_name}}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "portal",
    "aimmo_runner",
]

USE_I18N = True
USE_L10N = True

TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-gb"

PIPELINE_ENABLED = False
ROOT_URLCONF = "example_project.example_project.urls"
STATIC_ROOT = ".tests_static/"
SECRET_KEY = "test_key"
GAME_SERVER_URL_FUNCTION = lambda game_id: ("base %s" % game_id, "path %s" % game_id)
GAME_SERVER_PORT_FUNCTION = lambda game_id: 8001
GAME_SERVER_SSL_FLAG = False
from django_autoconfig.autoconfig import configure_settings  # noqa: E402

configure_settings(globals())
