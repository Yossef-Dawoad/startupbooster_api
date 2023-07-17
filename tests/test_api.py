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
    assert response.json() == {"message": "Hello World!"}


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
