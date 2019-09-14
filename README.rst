AutoREST
========

.. inclusion-marker-do-not-remove

.. image:: https://travis-ci.org/gregschmit/django-autorest.svg?branch=master
    :alt: TravisCI
    :target: https://travis-ci.org/gregschmit/django-autorest

.. image:: https://img.shields.io/pypi/v/django-autorest
    :alt: PyPI
    :target: https://pypi.org/project/django-autorest/

.. image:: https://coveralls.io/repos/github/gregschmit/django-autorest/badge.svg?branch=master
    :alt: Coveralls
    :target: https://coveralls.io/github/gregschmit/django-autorest?branch=master

.. image:: https://readthedocs.org/projects/django-autorest/badge/?version=latest
    :alt: Documentation Status
    :target: https://django-autorest.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style
    :target: https://github.com/ambv/black

Documentation: https://django-autorest.readthedocs.io

Source: https://github.com/gregschmit/django-autorest

PyPI: https://pypi.org/project/django-autorest/

AutoREST is a reusable Django app for building REST APIs from model definitions and
(optionally) ``admin.py`` definitions.

**The Problem**: Building APIs for models is boring.

**The Solution**: This app builds them for you, optionally using your AdminSite as a
guide, and you can just focus on the custom stuff.


How to Use
==========

.. code-block:: shell

    $ pip install django-autorest

Include ``autorest`` in your ``INSTALLED_APPS``.


Settings
--------

- ``AUTOREST_ADMIN_SITE`` (default ``'django.contrib.admin.site'``): This is an import
  string to the admin site where ``autorest`` can get hints on how the API should be
  configured (e.g., list display fields, edit fields, readonly fields, etc). To disable
  this feature entirely, just set this  to ``False``.
- ``AUTOREST_DEFAULT_USE_ADMIN_SITE`` (default ``False``): Whether the default model
  functionality should be to get config hints from ``admin.py``.
- ``AUTOREST_DEFAULT_ENABLE`` (default: ``True``): Whether API ViewSets/URLs should be
  built for models which don't have an explicit entry in the ``AUTOREST_CONFIG``. If
  this option is ``False``, then only models defined in the ``AUTOREST_CONFIG`` will
  have URLs generated for them.
- ``AUTOREST_CONFIG`` default:

.. code-block:: python

    {
        'auth': {
            'User': {
                'viewset': 'autorest.sample_user_viewset.UserViewSet',
            },
        },
    }


``AUTOREST_CONFIG`` Options:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``use_admin_site``: Whether to use the admin site to build the API.
- ``serializer``: An import string to a serializer instance. (Note: if you would use
  multiple serializers for different actions like list/detail, then you can use
  `drf-action-serializer <https://github.com/gregschmit/drf-action-serializer>`_) to
  configure a single serializer that supports per-action field configuration.)
- ``viewset``: An import string to a full viewset for this model.


Contributing
============

Submit a pull request if you would like to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must make any
contributions to this project available under the MIT license.

Development
===========

AutoREST comes with a ``settings.py`` file, allowing it to run as a standalone project.

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-autorest

Then you can go into the ``django-autorest`` directory and do the initial migrations and
run the server (you may need to type ``python3`` rather than ``python``):

.. code-block:: shell

    $ cd django-autorest
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the api at http://127.0.0.1:8000/api/.
