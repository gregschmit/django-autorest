AutoREST
########

.. inclusion-marker-do-not-remove

.. image:: https://readthedocs.org/projects/django-autorest/badge/?version=latest
    :target: https://django-purge.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Documentation: https://django-autorest.readthedocs.io

Source: https://github.com/gregschmit/django-autorest

PyPI: https://pypi.org/project/django-autorest/

AutoREST is a reusable Django app for building REST APIs from model definitions.

**The Problem**: Building APIs for models is boring.

**The Solution**: This app builds them for you and you can just focus on the
custom stuff.

How to Use
##########

.. code-block:: shell

    $ pip install django-autorest

Include ``autorest`` in your ``INSTALLED_APPS``. Then, in

Contributing
############

Email gschmi4@uic.edu if you want to contribute. You must only contribute code
that you have authored or otherwise hold the copyright to, and you must
make any contributions to this project available under the MIT license.

To collaborators: don't push using the ``--force`` option.

Dev Quickstart
##############

AutoREST comes with a ``settings.py`` file, technically making it a Django
project as well as a Django app. First clone, the repository into a location of
your choosing:

.. code-block:: shell

    $ git clone https://github.com/gregschmit/django-autorest

Then you can go into the :code:`django-autorest` directory and do the initial
migrations and run the server (you may need to type ``python3`` rather than
``python``):

.. code-block:: shell

    $ cd django-autorest
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createsuperuser
    ...
    $ python manage.py runserver

Then you can see the api at http://127.0.0.1:8000/api/.
