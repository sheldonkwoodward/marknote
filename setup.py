# sheldon woodward
# 9/6/18

"""Setuptools file."""

from os.path import abspath, dirname, join
from setuptools import find_packages, setup

from marknote import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='marknote',
    version=__version__,
    description='A simple note taking API for Django that supports creating notes and a folder structure. Built for '
                'the purpose of learning how to use the Django REST Framework to build a CRUD API.',
    long_description=long_description,
    url='https://github.com/sheldonkwoodward/marknote',
    author='Sheldon Woodward',
    author_email='contact@sheldonw.com',
    license='MIT',
    packages=find_packages(exclude=['django_server*']),
    classifiers=[
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='django rest api notes',
    python_requires='>=3.5',
    install_requires=[
        'django',
        'djangorestframework'
    ]
)

