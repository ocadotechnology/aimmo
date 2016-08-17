DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
INSTALLED_APPS = [
    'django.contrib.admin',
    'players',
]
PIPELINE_ENABLED = False
ROOT_URLCONF = 'django_autoconfig.autourlconf'
STATIC_ROOT = '.tests_static/'

from django_autoconfig.autoconfig import configure_settings
configure_settings(globals())
