import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-pressroom",
    version = "0.4.2",
    url = 'https://github.com/petry/django-pressroom',
    license = 'BSD',
    description = "A pressroom application for django.",

    author = 'Justin Driscoll, Michael Thornhill, Marcos Daniel Petry',
    author_email = 'marcospetry@gmail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools', 'django-photologue'],

    classifiers = [
        'Development Status :: 4.1 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
