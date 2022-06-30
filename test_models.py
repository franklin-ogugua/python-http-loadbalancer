import pytest
import responses

from models import Server


@pytest.fixture
def server():
    server = Server('localhost:5555')
    yield server


@responses.activate
def test_server_healthcheck_pass(server):
    responses.add(responses.GET, 'http://localhost:5555/healthcheck', status=200)
    server.healthcheck_and_update_status()
    assert server.healthy


@responses.activate
def test_server_healthcheck_fail(server):
    responses.add(responses.GET, 'http://localhost:5555/healthcheck', status=500)
    server.healthcheck_and_update_status()
    assert not server.healthy


def test_server_equal(server):
    another = Server('localhost:5554')
    assert server != another


def test_server_not_equal(server):
    another = Server('localhost:5555')
    assert server == another
