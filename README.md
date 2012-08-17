# Pressroom


Simple article management for the Django web framework.

[![Build Status](https://secure.travis-ci.org/petry/django-pressroom.png?branch=master)](http://travis-ci.org/petry/django-pressroom)


## Installation

Offical releases are available from http://pypi.python.org/pypi

```bash
easy_install django-pressroom
```

### Tracking the Development Version

The current development version of Pressroom can be checked out via Subversion from the project site using the following command:

```bash
git clone https://github.com/mthornhill/django-pressroom.git
```

If you wish to contribute to pressroom, here is how to set up your development environment

```bash
cd django-pressroom
virtualenv . --no-site-packages
source bin/activate
python bootstrap.py
bin/buildout -v
bin/django syncdb
bin/django runscript load_data -v2
bin/django runserver
```
browse to `http://localhost:8000/`


### Configure Your Django Settings

Add 'pressroom' to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = (
    # ...other installed applications,
    'photologue',
    'pressroom',
)
```

_Confirm that your `MEDIA_ROOT`, `MEDIA_URL`, `STATIC_ROOT`, `STATIC_URL` settings are correct._

### Sync Your Database

Run the Django `syncdb` command to create the appropriate tables.


## Instant Pressroom


To use the included pressroom templates and views you need to first add pressroom to your projects urls.py file.
Note: django-photologue (http://code.google.com/p/django-photologue/) is a dependancy of pressroom

```python
# urls.py:
urlpatterns += patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^pressroom/', include('pressroom.urls')),
    (r'^photologue/', include('photologue.urls')),
)
```
