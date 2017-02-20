===============
WSGI Basic Auth
===============

Really simple wsgi middleware to provide basic http auth. It is intented to
work with environment variables. This makes it simple to use in a docker 
context.

Status
------

.. image:: https://readthedocs.org/projects/wsgi-basic-auth/badge/?version=latest
    :target: https://readthedocs.org/projects/wsgi-basic-auth/
   
.. image:: https://travis-ci.org/mvantellingen/wsgi-basic-auth.svg?branch=master
    :target: https://travis-ci.org/mvantellingen/wsgi-basic-auth

.. image:: https://ci.appveyor.com/api/projects/status/im609ng9h29vt89r?svg=true
    :target: https://ci.appveyor.com/project/mvantellingen/wsgi-basic-auth

.. image:: http://codecov.io/github/mvantellingen/wsgi-basic-auth/coverage.svg?branch=master 
    :target: http://codecov.io/github/mvantellingen/wsgi-basic-auth?branch=master

.. image:: https://img.shields.io/pypi/v/wsgi-basic-auth.svg
    :target: https://pypi.python.org/pypi/wsgi-basic-auth/



Getting started
===============

Using this module is really simple.  In Django for example edit the wsgi.py
file and add the following to the end of the file.

.. code-block:: python

  from wsgi_basic_auth import BasicAuth 
  application = BasicAuth(application) 
  
Now run docker with the env variable WSGI_AUTH_CREDENTIALS=foo:bar and you have
to authenticate with username foo and password bar. Multiple credentials are
separated with a | (pipe) character.

To exclude specific paths for healthchecks (e.g. the Amazon ELB healthchecks)
specify the environment variable WSGI_AUTH_EXCLUDE_PATHS=/api/healthchecks.
Here multiple paths can be separated with the ; char.

To include only specific paths specify the environment variable
WSGI_AUTH_EXCLUDE_PATHS. Here multiple paths can be separated with the ; char.

You can use both include and exclude paths together for example:
WSGI_AUTH_PATHS=/foo
WSGI_AUTH_EXCLUDE_PATHS=/foo/bar
This will force Basic Auth on all paths under /foo except /foo/bar


Installation 
============

You can install the latest version using pip::

    pip install wsgi-basic-auth


