"""aimmo autoconfig"""
from common.app_settings import domain, MODULE_NAME

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
    # ----------------------------------------------------------------------------------
    # CSP CONFIG
    # ----------------------------------------------------------------------------------
    "CSP_DEFAULT_SRC": ("'self'",),
    "CSP_IMG_SRC": (
        f"{domain()}/static/",
        "https://p.typekit.net/",
    ),
    "CSP_FONT_SRC": (
        "https://use.typekit.net/",
    ),
    "CSP_SCRIPT_SRC": (
        "https://use.typekit.net/mrl4ieu.js",
        "https://pyodide-cdn2.iodide.io/v0.15.0/full/",
    ),
    "CSP_CONNECT_SRC": (
        "ws://localhost:41949/",
        "https://pyodide-cdn2.iodide.io/v0.15.0/full/",
        "ws://192.168.58.2:7959/socket.io/",
        "http://192.168.58.2:7959/socket.io/",
        f"https://{MODULE_NAME}-aimmo.codeforlife.education/",
        f"wss://{MODULE_NAME}-aimmo.codeforlife.education/",
    ),
    "CSP_REPORT_ONLY": False,
}
