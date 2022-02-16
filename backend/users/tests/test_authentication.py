import jwt

from django.conf import settings
import pytest


@pytest.mark.django_db
def test_get_token_url_unsuccessful_requirement_fields(client):
    response = client.post("/users/auth/token/create/")
    data = response.json()

    assert response.status_code == 400
    assert data == {
        "email": ["This field is required."],
        "password": ["This field is required."],
    }


@pytest.mark.django_db
def test_get_token_url_unsuccessful_wrongs_credentials(client):
    response = client.post(
        "/users/auth/token/create/",
        data={
            "email": "someweirdemail@email.com",
            "password": "mypasswordisbar",
        },
    )
    data = response.json()

    assert response.status_code == 401
    assert "access" not in data.keys()
    assert "refresh" not in data.keys()
    assert (
        data["detail"] == "No active account found with the given credentials"
    )


@pytest.mark.django_db
def test_get_token_successful(client, user):
    response = client.post(
        "/users/auth/token/create/",
        data={
            "email": user.email,
            "password": "mypassword",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "access" in data.keys()
    assert "refresh" in data.keys()


@pytest.mark.django_db
def test_refresh_token_successful(client, user):
    response = client.post(
        "/users/auth/token/create/",
        data={
            "email": user.email,
            "password": "mypassword",
        },
    )
    data = response.json()

    refresh = data["refresh"]
    response = client.post(
        "/users/auth/token/refresh/",
        data={
            "refresh": refresh,
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "access" in data.keys()


@pytest.mark.django_db
def test_refresh_token_unsuccessful(client):
    response = client.post(
        "/users/auth/token/refresh/",
        data={
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl9"  # noqa: 501
            "0eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2Nyw"  # noqa: 501
            "ianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJ"  # noqa: 501
            "joWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4",
        },
    )
    data = response.json()

    assert response.status_code == 401
    assert "access" not in data.keys()


@pytest.mark.django_db
def test_jwt_serializer(client, user):
    response = client.post(
        "/users/auth/token/create/",
        data={
            "email": user.email,
            "password": "mypassword",
        },
    )
    data = response.json()

    result = jwt.decode(
        data["access"],
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    assert response.status_code == 200
    assert "first_name" in result
    assert "last_name" in result
