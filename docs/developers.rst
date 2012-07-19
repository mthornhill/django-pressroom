Developers
===============

Tracking the Development Version
--------------------------------

The current development version of django-pressroom can be checked out via git from the project site using the following command:

    git clone https://github.com/mthornhill/django-pressroom.git

If you wish to contribute to pressroom, here is how to set up your development environment::

    cd django-pressroom
    virtualenv . --no-site-packages
    source bin/activate
    mkdir dlcache
    python bootstrap.py
    bin/buildout -v
    ./setupdatabase.sh
    bin/django runserver

browse to http://localhost:8000/ where you should be greeted by some dummy content.