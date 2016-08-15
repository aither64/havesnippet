===========
HaveSnippet
===========

HaveSnippet is a self-hosted paste service written in Python using the Django
framework.

--------
Features
--------

* As little overhead as possible
* Syntax highlight using pygments
* Optional limit on paste expiration for anonymous users
* Simple API, authentication with API keys
* `CLI client`_

See it running at https://paste.vpsfree.cz.

------------
Requirements
------------

* Python 3.4
* Django 1.10, might work with other versions
* See ``requirements.txt``

------------
Installation
------------

Clone this repository and create ``havesnippet/local_settings.py``. You should
set ``ALLOWED_HOSTS``, ``DATABASES``, ``SECRET_KEY`` and possibly
``STATIC_ROOT``, see Django documentation for more information about these.

Next, run database migrations::

    $ python manage.py migrate --settings=havesnippet.local_settings

It is necessary to install languages to database::

    $ python manage.py loadlanguages all --settings=havesnippet.local_settings

Then you can try the development server::

    $ python manage.py runserver --settings=havesnippet.local_settings

-------------
Configuration
-------------

Expired snippets are deleted using manage.py command ``expiresnippets``::

    $ python manage.py expiresnippets --settings=havesnippet.local_settings

This command should be called in regularly, e.g. every 10 minutes.

Application settings:

* ``SNIPPET_PASTE_PUBLIC`` - ``True`` or ``False``, enable/disable paste for
  anonymous users (``False``)
* ``SNIPPET_PUBLIC_MAX_EXPIRATION`` - Integer, max expiration for anonymous
  users in seconds. ``False`` disables this limit. (``False``)
* ``SNIPPET_SLUG_LENGTH`` - the length of snippet slug in URL (8)
* ``SNIPPET_SLUG_CHARS`` - a string of characters that can appear in the slug

.. _CLI client: https://github.com/aither64/havesnippet-client
