import os
print "TOP OF SETTINGS FILE"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite3'),
    },
}
print "SETUP DB"
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'players',
    'integration_tests',
    'aimmo_runner',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'views': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    }
}

print "SETUP INSTALLED APPS"
PIPELINE_ENABLED = False
ROOT_URLCONF = 'django_autoconfig.autourlconf'
STATIC_ROOT = '.tests_static/'
SECRET_KEY = 'test_key'
print "SETUP KEY"
GAME_SERVER_URL_FUNCTION = lambda game_id: ('base %s' % game_id, 'path %s' % game_id)
GAME_SERVER_PORT_FUNCTION = lambda game_id: 8001
GAME_SERVER_SSL_FLAG = False
print "SETUP GAME SERVER STUFF"
from django_autoconfig.autoconfig import configure_settings  # noqa: E402
configure_settings(globals())
print "SETUP GLOBAL CONFIGURATIONS"