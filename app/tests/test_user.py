from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from app.core.user_management import UserRegister


def test_hello(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"


def test_register(client: FlaskClient, mocker: MockerFixture):
    user_register_mock = mocker.patch(
        "app.api.user_management.user_management.core_user_register", return_value={}
    )
    response = client.post(
        "/register",
        data={
            "email": "custom.emai@server.com",
            "username": "dummy_user",
            "password_hash": "hash_password",
        },
    )
    user_register_mock.assert_called_once_with(
        UserRegister(
            email="custom.emai@server.com",
            password_hash="hash_password",
            username="dummy_user",
        )
    )
    assert response.status_code == 200


def test_circleci():
    assert 1 == 2

