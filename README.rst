AutoREST
========

.. inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/gregschmit/django-autorest.svg?branch=master
    :target: https://travis-ci.org/gregschmit/django-autorest

.. image:: https://img.shields.io/pypi/v/django-autorest
    :alt: PyPI

.. image:: https://coveralls.io/repos/github/gregschmit/django-autorest/badge.svg?branch=master
    :target: https://coveralls.io/github/gregschmit/django-autorest?branch=master

.. image:: https://readthedocs.org/projects/django-autorest/badge/?version=latest
    :target: https://django-autorest.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Documentation: https://django-autorest.readthedocs.io

Source: https://github.com/gregschmit/django-autorest

PyPI: https://pypi.org/project/django-autorest/

AutoREST is a reusable Django app for building REST APIs from model definitions
and (optionally) ``admin.py`` definitions.

**The Problem**: Building APIs for models is boring.

**The Solution**: This app builds them for you, optionally using your AdminSite
as a guide, and you can just focus on the custom stuff.


How to Use
==========

.. code-block:: shell

    $ pip install django-autorest

Include ``autorest`` in your ``INSTALLED_APPS``.


Settings
--------

* ``AUTOREST_ADMIN_SITE`` (default ``'django.contrib.admin.site'``): This is
  an import string to the admin site where ``autorest`` can get hints on how the
  API should be configured (e.g., list display fields, edit fields, readonly
  fields, etc). To disable this feature entirely, just set this  to ``False``.
* ``AUTOREST_DEFAULT_USE_ADMIN_SITE`` (default ``False``): Whether the default
  model functionality should be to get config hints from ``admin.py``.
* ``AUTOREST_DEFAULT_ENABLE`` (default: ``True``): Whether API ViewSets/URLs
  should be built for models which don't have an explicit entry in the
  ``AUTOREST_CONFIG``. If this option is ``False``, then only models defined in
  the ``AUTOREST_CONFIG`` will have URLs generated for them.
* ``AUTOREST_CONFIG`` default:

.. code-block:: python

    {
        'auth': {
            'Group': {
                'use_admin_site': True,
            },
            'User': {
                'viewset': 'autorest.sample_user_viewset.UserViewSet',
            },
        },
    }


``AUTOREST_CONFIG`` Options:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``use_admin_site``: Whether to use the admin site to build the API.
* ``serializer``: An import string to a serializer instance.
* ``list_serializer``: An import string to a serializer instance (usually
    providing less fields available in the listing).
* ``viewset``: An import string to a full viewset for this model.


Contributing
============

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the ``--force`` option.

Dev Quickstart
==============

AutoREST comes with a ``settings.py`` file, technically making it a Django
project as well as a Django app. First clone, the repository into a location of
your choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-autorest

Then you can go into the ``django-autorest`` directory and do the initial
migrations and run the server (you may need to type ``python3`` rather than
``python``):

.. code-block:: shell

    $ cd django-autorest
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the api at http://127.0.0.1:8000/api/.

To Do
=====

- Build endpoints based on ``admin.py`` configuration (this should be optional, using a ``settings.py`` switch, like ``AUTOREST_USE_ADMIN_PY``)
  - Rigth now, simple models like the ``auth.Group`` work, however complex models like the ``auth.User`` don't because the create API endpoint should take password/confirmation not the raw password hash.
- Build CRUD forms for the endpoints (maybe a generator)
