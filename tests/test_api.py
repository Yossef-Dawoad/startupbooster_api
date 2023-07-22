# from typing import assert_types ## py3.11

from fastapi import status
from fastapi.testclient import TestClient

# we had to have __init__.py in the current directory
# this will make the current module a package
from api.main import app

client = TestClient(app=app)
StringArray = list[str]


def test_index_correct_response() -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_api_generate_keywords() -> None:
    response = client.get(
        "/api/v1/keywords",
        params={"prompt": "coffee"},
    )
    res_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "kw" in res_data
    assert (
        isinstance(res_data["kw"], list) and len(res_data["kw"]) > 0
    ), "No keywords generated"


def test_api_generate_business_seo() -> None:
    response = client.get(
        "/api/v1/business",
        params={"prompt": "coffee"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "keywords" in response.json() and len(response.json()["keywords"]) > 0
    assert "snippet" in response.json() and len(response.json()["snippet"]) > 0


def test_get_token() -> None:
    user_auth_data = {
        "username": "yaasadgvfdousfsef",
        "password": "mywarrprarsfdhgjmscode",
        "email": "qoaudgasetty@email.com",
    }
    user_register = client.post(
        "/auth/register",
        json=user_auth_data,
    ).json()
    if ("detail" in user_register) & (
        user_register["detail"] == "username already registered"
    ):
        user_register = {
            "username": user_auth_data["username"],
            "password": user_auth_data["password"],
        }
    else:
        # send a request with valid credentials to get a token
        response = client.post(
            "/auth/token",
            json={
                "username": user_register["username"],
                "password": user_register["password"],
            },
        )
        # assert that the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK
        # assert that the response contains an access token of type "bearer"
        assert response.json()["token_type"] == "bearer"
        assert "x-process-time" in response.headers()
        assert "access_token" in response.json()


def test_read_items_unauthorized() -> None:
    # send a request without a token to read items
    response = client.get("/auth/users/me")
    # assert that the response status code is 401 Unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    # assert that the response contains the expected error message
    assert response.json() == {"detail": "Not authenticated"}
