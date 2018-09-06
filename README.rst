MarkNote
--------
|Build Status|
|Codacy Quality Badge|
|Codacy Coverage Badge|

A simple note taking API for Django that supports creating notes and a folder structure. Built for the purpose of learning how to use the Django REST Framework to build a CRUD API.

Endpoints
=========
There are four different endpoints for the API. The ``marknote`` portion of the URI can be mapped using the Django urls.py file. It is setup as show in the sample project. Refer to the ``docs`` folder for a complete API specification.

- ``/marknote/note``
- ``/marknote/note/{id}``
- ``/marknote/folder``
- ``/marknote/folder/{id}``

/marknote/note
++++++++++++++
The create and list endpoint used to create and list all notes.

/marknote/note/{id}
+++++++++++++++++++
The retrieve, update, and destroy endpoint used to access individual notes.

/marknote/folder
++++++++++++++++
The create and list endpoint used to create and list all folders.

/marknote/folder/{id}
+++++++++++++++++++++
The retrieve, update, and destroy endpoint used to access individual folders.


.. |Build Status| image:: https://travis-ci.org/sheldonkwoodward/marknote.svg?branch=master
    :target: https://travis-ci.org/sheldonkwoodward/marknote

.. |Codacy Quality Badge| image:: https://api.codacy.com/project/badge/Grade/171d5b34125f45e6970a10806dc0ea02
    :target: https://www.codacy.com/app/sheldonkwoodward/marknote?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sheldonkwoodward/marknote&amp;utm_campaign=Badge_Grade

.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/171d5b34125f45e6970a10806dc0ea02
    :target: https://www.codacy.com/app/sheldonkwoodward/marknote?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sheldonkwoodward/marknote&amp;utm_campaign=Badge_Coverage
