# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.get_all_payloads200_response import GetAllPayloads200Response  # noqa: F401
from openapi_server.models.payload import Payload  # noqa: F401


def test_create_payload(client: TestClient):
    """Test case for create_payload

    Create a new payload
    """
    payload = {"passengers":155,"estimate4_timestamp":"2023-01-01T10:10:10Z","baggage":2510.5,"last_updated_on":"2023-01-01T10:10:10Z","id":1001,"cargo":1220.2}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/payloads",
    #    headers=headers,
    #    json=payload,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_payload(client: TestClient):
    """Test case for delete_payload

    Delete payload
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/payloads/{id}".format(id=1001),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_all_payloads(client: TestClient):
    """Test case for get_all_payloads

    List all payloads
    """
    params = [("offset", 0),     ("limit", 5)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/payloads",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_payload(client: TestClient):
    """Test case for get_payload

    Retrieve a payload by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/payloads/{id}".format(id=1001),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_payload(client: TestClient):
    """Test case for update_payload

    Update payload with actuals.
    """
    payload = {"passengers":155,"estimate4_timestamp":"2023-01-01T10:10:10Z","baggage":2510.5,"last_updated_on":"2023-01-01T10:10:10Z","id":1001,"cargo":1220.2}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/payloads/{id}".format(id=1001),
    #    headers=headers,
    #    json=payload,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

