import os
DIRNAME = os.path.dirname(__file__)
DEBUG=True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/tmp/pressroom.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = os.path.realpath(os.path.join(DIRNAME, 'tests', 'media/'))
MEDIA_URL = '/site_media/'
SITE_ID = 1
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, "tests", "templates"),
)
INSTALLED_APPS = [
                  'ajax_select',
                  'django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.comments',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.staticfiles',
                  'endless_pagination',
                  'haystack',
                  'imperavi',
                  'pressroom',
                  'photologue',
                  'south',
                  'tagging',]
ROOT_URLCONF = 'pressroom.tests.urls'

INTERNAL_IPS = ('127.0.0.1',)

# ajax-selects
# define the lookup channels in use on the site
AJAX_LOOKUP_CHANNELS = {
    #   pass a dict with the model and the field to search against
    'photos'  : ('pressroom.lookups', 'PhotoLookup'),
    'documents'  : ('pressroom.lookups', 'DocumentLookup'),
}

# magically include jqueryUI/js/css
AJAX_SELECT_BOOTSTRAP = True
AJAX_SELECT_INLINES = 'inline'

# haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

