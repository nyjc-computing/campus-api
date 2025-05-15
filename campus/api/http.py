"""campus/api/http

Implements HTTP calls for the Campus API.
"""

import logging
from typing import Callable

import requests

from .base import JsonSerializable


class HttpError(Exception):
    """Custom exception for HTTP errors."""

    def __init__(self, message: str, response: requests.Response):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.text = response.text


def _log_response(response: requests.Response) -> None:
    """Display the response from the Campus API.
    Displays an error message if the response is not successful.

    Args:
        response (requests.Response): The response object from the API call.
    """
    _req = response.request
    log_str = f"{_req.method} {_req.url} {response.status_code}"
    logging.debug(log_str)


def _call_api(
        method: str,
        url: str,
        data: dict | None,
        callback: Callable[[requests.Response], None] = _log_response,
) -> JsonSerializable:
    """Make an API call to the Campus API.

    Args:
        method (str): The HTTP method to use (GET, POST, PUT, DELETE).
        url (str): The URL for the API endpoint.
        data (dict, optional): The data to send in the request body. Defaults to None.

    Returns:
        requests.Response: The response object from the API call.
    """
    response = (
        requests.request(method, url, json=data) if data
        else requests.request(method, url)
    )
    callback(response)
    return response.json()


def get(url: str) -> JsonSerializable:
    """Make a GET request to the Campus API.

    Args:
        url (str): The URL for the API endpoint.
        params (dict, optional): The query parameters to include in the request. Defaults to None.

    Returns:
        JsonSerializable: The JSON response from the API.
    """
    return _call_api("GET", url, None)

def post(url: str, data: dict | None = None) -> JsonSerializable:
    """Make a POST request to the Campus API.

    Args:
        url (str): The URL for the API endpoint.
        data (dict): The data to send in the request body.

    Returns:
        JsonSerializable: The JSON response from the API.
    """
    return _call_api("POST", url, data)

def put(url: str, data: dict | None = None) -> JsonSerializable:
    """Make a PUT request to the Campus API.

    Args:
        url (str): The URL for the API endpoint.
        data (dict): The data to send in the request body.

    Returns:
        JsonSerializable: The JSON response from the API.
    """
    return _call_api("PUT", url, data)

def delete(url: str) -> JsonSerializable:
    """Make a DELETE request to the Campus API.

    Args:
        url (str): The URL for the API endpoint.

    Returns:
        JsonSerializable: The JSON response from the API.
    """
    return _call_api("DELETE", url)

def patch(url: str, data: dict | None = None) -> JsonSerializable:
    """Make a PATCH request to the Campus API.

    Args:
        url (str): The URL for the API endpoint.
        data (dict): The data to send in the request body.

    Returns:
        JsonSerializable: The JSON response from the API.
    """
    return _call_api("PATCH", url, data)
