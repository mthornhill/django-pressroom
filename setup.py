from setuptools import setup, find_packages

setup(
    name = "django-pressroom",
    version = "0.1",
    url = 'http://code.google.com/p/django-pressroom/',
    license = 'BSD',
    description = "A pressroom application for django.",
    author = 'Justin Driscoll',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
