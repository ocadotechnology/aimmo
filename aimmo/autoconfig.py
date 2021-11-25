"""aimmo autoconfig"""

from .csp_config import CSP_CONFIG

DEFAULT_SETTINGS = {"AUTOCONFIG_INDEX_VIEW": "aimmo/home", "STATIC_URL": "/static/"}

SETTINGS = {
    "INSTALLED_APPS": [
        "common",
        "django.contrib.auth",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_js_reverse",
        "rest_framework",
    ],
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ],
    "USE_TZ": True,
}

SETTINGS.update(CSP_CONFIG)
