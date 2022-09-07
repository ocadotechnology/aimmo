import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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

PIPELINE_ENABLED = False
ROOT_URLCONF = "example_project.urls"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "aimmo/static")]
SECRET_KEY = "bad_test_secret"

WSGI_APPLICATION = "wsgi.application"

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

GAME_SERVER_URL_FUNCTION = lambda game_id: ("base %s" % game_id, "path %s" % game_id)
GAME_SERVER_PORT_FUNCTION = lambda game_id: 8001
GAME_SERVER_SSL_FLAG = False

CLOUD_STORAGE_PREFIX = "https://storage.googleapis.com/codeforlife-assets/"
SITE_ID = 1
