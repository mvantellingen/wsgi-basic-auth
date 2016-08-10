import pytest
import wsgi_basic_auth
from webtest import TestApp, AppError


def wsgi_app(environ, start_response):
    body = 'this is private! go away!'
    headers = [
        ('Content-Type', 'text/html; charset=utf8'),
        ('Content-Length', str(len(body)))
    ]
    start_response('200 OK', headers)
    return [body]


def test_no_auth(monkeypatch):
    monkeypatch.delenv('WSGI_AUTH_CREDENTIALS', None)
    application = wsgi_basic_auth.BasicAuth(wsgi_app)
    app = TestApp(application)
    response = app.get('/')
    assert response.status_code == 200


def test_auth(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_CREDENTIALS', 'foo:bar')
    application = wsgi_basic_auth.BasicAuth(wsgi_app)
    app = TestApp(application)
    app.get('/', status=401)

    app.authorization = ('Basic', ('foo', 'bar'))
    app.get('/', status=200)


def test_auth_exclude(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_CREDENTIALS', 'foo:bar')
    monkeypatch.setenv('WSGI_AUTH_EXCLUDE_PATHS', '/healthcheck')
    application = wsgi_basic_auth.BasicAuth(wsgi_app)
    app = TestApp(application)
    app.get('/', status=401)
    app.get('/healthcheck/foo', status=200)


def test_users_from_environ(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_CREDENTIALS', 'foo:bar')
    result = wsgi_basic_auth._users_from_environ()
    assert result == {'foo': 'bar'}


def test_users_from_environ_none(monkeypatch):
    monkeypatch.delenv('WSGI_AUTH_CREDENTIALS', None)
    result = wsgi_basic_auth._users_from_environ()
    assert result == {}


def test_users_from_environ_empty(monkeypatch):
    monkeypatch.delenv('WSGI_AUTH_CREDENTIALS', '')
    result = wsgi_basic_auth._users_from_environ()
    assert result == {}


def test_users_from_environ_multiple(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_CREDENTIALS', 'foo:bar|bar:foo')
    result = wsgi_basic_auth._users_from_environ()
    assert result == {'foo': 'bar', 'bar': 'foo'}


def test_exclude_paths_from_environ(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_EXCLUDE_PATHS', '/foo/bar')
    result = wsgi_basic_auth._exclude_paths_from_environ()
    assert result == ['/foo/bar']


def test_exclude_paths_from_environ_none(monkeypatch):
    monkeypatch.delenv('WSGI_AUTH_EXCLUDE_PATHS', None)
    result = wsgi_basic_auth._exclude_paths_from_environ()
    assert result == []


def test_exclude_paths_from_environ_empty(monkeypatch):
    monkeypatch.delenv('WSGI_AUTH_EXCLUDE_PATHS', '')
    result = wsgi_basic_auth._exclude_paths_from_environ()
    assert result == []


def test_exclude_paths_from_environ_multiple(monkeypatch):
    monkeypatch.setenv('WSGI_AUTH_EXCLUDE_PATHS', '/foo/bar;/bar/foo')
    result = wsgi_basic_auth._exclude_paths_from_environ()
    assert result == ['/foo/bar', '/bar/foo']
