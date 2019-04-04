import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.sqlite3"),
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "aimmo",
    "integration_tests",
    "aimmo_runner",
]

PIPELINE_ENABLED = False
ROOT_URLCONF = "django_autoconfig.autourlconf"
STATIC_ROOT = ".tests_static/"
SECRET_KEY = "test_key"
GAME_SERVER_URL_FUNCTION = lambda game_id: ("base %s" % game_id, "path %s" % game_id)
GAME_SERVER_PORT_FUNCTION = lambda game_id: 8001
GAME_SERVER_SSL_FLAG = False
from django_autoconfig.autoconfig import configure_settings  # noqa: E402

configure_settings(globals())
