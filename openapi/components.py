"""openapi/components

Classes for representing the components section of OpenAPI.
"""

from .datatypes import Schema
from .path import Parameter
from .request import RequestBody
from .response import Response


class Components:
    """Represents a collection of components as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/components/
    """
    schemas: list[Schema]
    parameters: list[Parameter]
    securitySchemes: list
    requestBodies: list[RequestBody]
    responses: list[Response]
    headers: list
    examples: list
    links: list
    callbacks: list
