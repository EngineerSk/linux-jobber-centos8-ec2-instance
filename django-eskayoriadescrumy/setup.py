import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-eskayoriadescrumy",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license="",
    description="A simple django app",
    lang_description=README,
    url="https://www.example.com",
    author="DUROSINMI SIKIRU ORIADE",
    author_email="eskayoriade@gmail.com",
    classifiers = [
        'Evironment :: Web Environment',
        'Framework :: Django : 3.0',
        'Intended Audience :: Developers',
        'License :  :: ',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)