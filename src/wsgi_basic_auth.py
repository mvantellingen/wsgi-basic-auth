import os
from base64 import b64decode

from webob import Request
from webob.exc import HTTPUnauthorized

__version__ = '1.1.0'


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
                          environment variable are used (splitted by ``;``)
    :param include_paths: list of path prefixes to include in auth. When not
                          supplied the values from the ``WSGI_AUTH_PATHS``
                          environment variable are used (splitted by ``;``)
    :param env_prefix: prefix for the environment variables above, default ``''``

    """

    def __init__(self, app, realm='Protected', users=None, exclude_paths=None,
                 include_paths=None, env_prefix=''):
        self._app = app
        self._env_prefix = env_prefix
        self._realm = realm
        self._users = users or _users_from_environ(env_prefix)
        self._exclude_paths = set(
            exclude_paths or _exclude_paths_from_environ(env_prefix))
        self._include_paths = set(
            include_paths or _include_paths_from_environ(env_prefix))

    def __call__(self, environ, start_response):
        if self._users:
            request = Request(environ)
            if not self.is_authorized(request):
                return self._login(environ, start_response)
        return self._app(environ, start_response)

    def is_authorized(self, request):
        """Check if the user is authenticated for the given request.

        The include_paths and exclude_paths are first checked. If
        authentication is required then the Authorization HTTP header is
        checked against the credentials.

        """
        if self._is_request_in_include_path(request):
            if self._is_request_in_exclude_path(request):
                return True
            else:
                auth = request.authorization
                if auth and auth[0] == 'Basic':
                    credentials = b64decode(auth[1]).decode('UTF-8')
                    username, password = credentials.split(':', 1)
                    return self._users.get(username) == password
                else:
                    return False
        else:
            return True

    def _login(self, environ, start_response):
        """Send a login response back to the client."""
        response = HTTPUnauthorized()
        response.www_authenticate = ('Basic', {'realm': self._realm})
        return response(environ, start_response)

    def _is_request_in_include_path(self, request):
        """Check if the request path is in the `_include_paths` list.

        If no specific include paths are given then we assume that
        authentication is required for all paths.

        """
        if self._include_paths:
            for path in self._include_paths:
                if request.path.startswith(path):
                    return True
            return False
        else:
            return True

    def _is_request_in_exclude_path(self, request):
        """Check if the request path is in the `_exclude_paths` list"""
        if self._exclude_paths:
            for path in self._exclude_paths:
                if request.path.startswith(path):
                    return True
            return False
        else:
            return False


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
    """Environment value via `/login;/register`"""
    paths = os.environ.get(env_prefix + 'WSGI_AUTH_EXCLUDE_PATHS')
    if not paths:
        return []
    return paths.split(';')


def _include_paths_from_environ(env_prefix=''):
    """Environment value via `/login;/register`"""
    paths = os.environ.get(env_prefix + 'WSGI_AUTH_PATHS')
    if not paths:
        return []
    return paths.split(';')
