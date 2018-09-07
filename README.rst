MarkNote
--------
|PyPI Version|
|Python Versions|
|Django Versions|
|License|
|Build Status|
|Codacy Quality Badge|
|Codacy Coverage Badge|

A simple note taking API for Django that supports creating notes and a folder structure. Built for the purpose of learning how to use the Django REST Framework to build a CRUD API.

Features
--------
- Notes and folder structure
- Per item owners
- Integrated Django permissions

**Planned Features**

- Revision history
- Bearer token support
- Note sharing
- Ownership transfer

Installation
------------
1. Install with pip.

::

    $ pip install marknote

2. Modify your ``INSTALLED_APPS`` in settings.py.

::

    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework.authtoken',
        'marknote',
    ]

3. Modify you ``urlpatterns`` in urls.py.

::

    from django.urls import include, re_path

    urlpatterns = [
        re_path(r'^marknote/', include(('marknote.urls', 'marknote'), namespace-'marknote'))
    ]

Endpoints
---------
Documentation can be found `here <https://app.swaggerhub.com/apis/sheldonkwoodward3/marknote/docs/>`_. Refer to the ``docs`` folder for the OpenAPI specification file.

There are four different endpoints for the API. The ``marknote`` portion of the URI can be mapped using the Django urls.py file. It is setup as shown in the sample project.

/marknote/note
  The create and list endpoint used to create and list all notes.

/marknote/note/{id}
  The retrieve, update, and destroy endpoint used to access individual notes.

/marknote/folder
  The create and list endpoint used to create and list all folders.

/marknote/folder/{id}
  The retrieve, update, and destroy endpoint used to access individual folders.
  
Tests
-----
To run the unit tests, simply use the Django test command with Pipenv.

::

    $ pipenv install
    $ pipenv run python manage.py test


.. |PyPI Version| image:: https://img.shields.io/pypi/v/marknote.svg
    :target: https://pypi.org/project/marknote/

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/marknote.svg

.. |Django Versions| image:: https://img.shields.io/pypi/djversions/marknote.svg

.. |License| image:: https://img.shields.io/github/license/sheldonkwoodward/marknote.svg
    :target: https://github.com/sheldonkwoodward/marknote/LICENSE.txt

.. |Build Status| image:: https://travis-ci.org/sheldonkwoodward/marknote.svg?branch-master
    :target: https://travis-ci.org/sheldonkwoodward/marknote

.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/171d5b34125f45e6970a10806dc0ea02
    :target: https://www.codacy.com/app/sheldonkwoodward/marknote?utm_source-github.com&amp;utm_medium-referral&amp;utm_content-sheldonkwoodward/marknote&amp;utm_campaign-Badge_Grade

.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/171d5b34125f45e6970a10806dc0ea02
    :target: https://www.codacy.com/app/sheldonkwoodward/marknote?utm_source-github.com&amp;utm_medium-referral&amp;utm_content-sheldonkwoodward/marknote&amp;utm_campaign-Badge_Coverage
