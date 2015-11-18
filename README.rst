wsgi-basic-auth
===============

Really simple wsgi middleware to provide basic http auth compatible with Amazon ELB. It is intented to work with environment variables within a docker context.

In Django for example edit the wsgi.py file and add the following to the end of the file.

.. code:: python

    from wsgi_basic_auth import BasicAuth
    application = BasicAuth(application)

Now run docker with the env variable `WSGI_AUTH_CREDENTIALS=foo:bar` and you have to authenticate with username `foo` and password `bar`. Multiple credentials are separated with a | (pipe) character.

To exclude specific paths for healthchecks (e.g. the Amazon ELB healthchecks) specifcy the environment variable `WSGI_AUTH_EXCLUDE_PATHS=/api/healthchecks`. Here multiple paths can be separated with the `;` char.
