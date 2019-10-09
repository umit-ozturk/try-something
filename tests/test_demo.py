import logging


log = logging.getLogger(__name__)


def test_ping(integration_client):
    ping = integration_client.get("/api/v1/ping")
    assert ping.status_code == 200, "Ping returned wrong status code"
    assert ping.data == b'{"response":"PONG"}\n', "Ping returned bad response."


def test_user_get_404(integration_client):
    user = integration_client.get("/api/v1/user/foo@bar.com")
    assert user.status_code == 404, "User 404 returned wrong status code"
    assert user.data == b'{"response":"Not Found"}\n', "User 404 returned bad response."


def test_user_get_success(integration_client):
    successful_data = b'{"account":"success@bar.com","active":true}\n'
    user = integration_client.get("/api/v1/user/success@bar.com")
    assert user.status_code == 200, "User success returned wrong status code"
    assert user.data == successful_data, "User success returned bad response."
