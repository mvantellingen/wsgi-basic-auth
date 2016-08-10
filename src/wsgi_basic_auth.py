import os
from base64 import b64decode

from webob import Request
from webob.exc import HTTPUnauthorized


class BasicAuth(object):
    """WSGI Middleware to add Basic Authentication to an existing wsgi app.

    :param app: the wsgi application
    :param realm: the basic auth realm. Default = 'protected'
    :param users: dictionary with username -> password mapping. When not
                  supplied the values from the environment variable
                  ``WSGI_AUTH_CREDENTIALS``. If no users are defined then
                  the middleware is disabled.

    :param exclude_paths: list of path prefixes to exclude from auth. When not
                          supplied the values from the ``WSGI_AUTH_EXCLUDE_PATHS``
                          environment variable are used (splitted by ``:``)
    :param env_prefix: prefix for the environment variables above, default ``''``

    """

    def __init__(self, app, realm='Protected', users=None, exclude_paths=None,
                 env_prefix=''):
        self._app = app
        self._env_prefix = env_prefix
        self._realm = realm
        self._users = users or _users_from_environ(env_prefix)
        self._exclude_paths = (
            exclude_paths or _exclude_paths_from_environ(env_prefix))

    def __call__(self, environ, start_response):
        if self._users:
            request = Request(environ)
            if not self.is_authorized(request):
                return self._login(environ, start_response)
        return self._app(environ, start_response)

    def is_authorized(self, request):
        auth = request.authorization
        for path in self._exclude_paths:
            if request.path.startswith(path):
                return True

        if auth and auth[0] == 'Basic':
            credentials = b64decode(auth[1]).decode('UTF-8')
            username, password = credentials.split(':', 1)
            return self._users.get(username) == password

        return False

    def _login(self, environ, start_response):
        response = HTTPUnauthorized()
        response.www_authenticate = ('Basic', {'realm': self._realm})
        return response(environ, start_response)


def _users_from_environ(env_prefix=''):
    """Environment value via `user:password|user2:password2`"""
    auth_string = os.environ.get(env_prefix + 'WSGI_AUTH_CREDENTIALS')
    if not auth_string:
        return {}

    result = {}
    for credentials in auth_string.split('|'):
        username, password = credentials.split(':', 1)
        result[username] = password
    return result


def _exclude_paths_from_environ(env_prefix=''):
    """Environment value via `user:password|user2:password2`"""
    paths = os.environ.get(env_prefix + 'WSGI_AUTH_EXCLUDE_PATHS')
    if not paths:
        return []
    return paths.split(';')
