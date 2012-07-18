Getting started
===============

Requirements
~~~~~~~~~~~~

======  ======
Python  >= 2.5
Django  >= 1.4
django-imperavi
django-ajax-selects
django-photologue
django-extensions
django-haystack
django-endless-pagination
south
django-tagging
django-taggit
======  ======

Installation
~~~~~~~~~~~~

easy_install django-pressroom

Settings
~~~~~~~~

Add the following to your *settings.py*, e.g.::

    # ajax-selects
    # define the lookup channels in use on the site
    AJAX_LOOKUP_CHANNELS = {
        #   pass a dict with the model and the field to search against
        'photos'  : ('pressroom.lookups', 'PhotoLookup'),
        'documents'  : ('pressroom.lookups', 'DocumentLookup'),
        'articles'  : ('pressroom.lookups', 'ArticleLookup'),
        }

    # magically include jqueryUI/js/css
    AJAX_SELECT_BOOTSTRAP = True
    AJAX_SELECT_INLINES = 'inline'

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
        )

Add::

    'ajax_select',
    'bootstrapped',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'endless_pagination',
    'haystack',
    'imperavi',
    'pressroom',
    'photologue',
    'south',
    'tagging',
    'taggit',


to the ``INSTALLED_APPS`` in your *settings.py* if they don't exist already.


Quickstart
~~~~~~~~~~

Sync Your Database
------------------

Run the Django 'syncdb' command to create the appropriate tables.
or
Run Django 'migrate' (from south) to migrate an existing pressroom database.

Instant Pressroom
---------------------

To use the included pressroom templates and views you need to first add pressroom to your projects urls.py file.
Note: django-photologue (http://code.google.com/p/django-photologue/) is a dependancy of pressroom::

    # urls.py:
    urlpatterns += patterns('',
        (r'^admin/(.*)', admin.site.root),
        (r'^pressroom/', include('pressroom.urls')),
        (r'^photologue/', include('photologue.urls')),
        (r'^imperavi/', include('imperavi.urls')),
        (r'^search/', include('haystack.urls')),
        (r'^comments/', include('django.contrib.comments.urls')),
    )

