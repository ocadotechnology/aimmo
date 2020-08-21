DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

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
                "portal.context_processors.process_newsletter_form",
            ]
        },
    }
]

INSTALLED_APPS = ["portal"]
PIPELINE_ENABLED = False
ROOT_URLCONF = "example_project.example_project.urls"
STATIC_ROOT = "example_project/example_project/static"
SECRET_KEY = "bad_test_secret"

GAME_SERVER_URL_FUNCTION = lambda game_id: ("base %s" % game_id, "path %s" % game_id)
GAME_SERVER_PORT_FUNCTION = lambda game_id: 8001
GAME_SERVER_SSL_FLAG = False
from django_autoconfig.autoconfig import configure_settings  # noqa: E402

configure_settings(globals())
