from pytest_httpserver import HTTPServer
from external.client import UserClient

def test_fetch_user_from_external_api(httpserver: HTTPServer):
    httpserver.expect_request("/users/1").respond_with_json(
        {"id": 1, "first": "Ada", "last": "Lovelace"}, status=200
    )
    client = UserClient(httpserver.url_for(""))
    user = client.fetch_user(1)

    assert user is not None
    assert user["id"] == 1
    assert user["first"] == "Ada"
    assert user["last"] == "Lovelace"

def test_returns_none_on_404(httpserver: HTTPServer):
    httpserver.expect_request("/users/999").respond_with_data(status=404)
    client = UserClient(httpserver.url_for(""))
    assert client.fetch_user(999) is None

def test_returns_none_when_fields_missing_for_user_six(httpserver: HTTPServer):
    # Prueba específica para el ID 6 aplicando la regla de campos faltantes ('first' o 'last')
    httpserver.expect_request("/users/6").respond_with_json(
        {"id": 6, "first": "Incompleto"}, status=200
    )
    client = UserClient(httpserver.url_for(""))
    assert client.fetch_user(6) is None