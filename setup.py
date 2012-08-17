import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-pressroom",
    version = "0.7",
    url = 'http://code.google.com/p/django-pressroom/',
    license = 'BSD',
    description = "A pressroom application for django.",
    long_description = read('README.md'),

    author = 'Justin Driscoll, Michael Thornhill',
    author_email = 'michael@maithu.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools',
                        'django-photologue',
                        'django-extensions',
                        'django-ajax-selects',
                        'django-endless-pagination',
                        'django-imperavi',
                        'django-reversion',
                        'django-taggit'
    ],
    include_package_data=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
