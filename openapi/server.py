"""openapi/server

Classes for representing API servers
"""

from typing import Mapping, Sequence


class ServerVariable:
    """Represents a server variable as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/api-host-and-base-path/
    """
    default: str
    enum: tuple[str] = ()

    def __init__(self, default: str, description: str | None = None, *, enum: Sequence[str] = ()):
        self.default = default
        self.enum = tuple(enum)


class Server:
    """Represents a server entry as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/api-host-and-base-path/
    """
    url: str
    description: str

    def __init__(self, url: str, description: str | None = None, **variables: ServerVariable):
        # TODO: validate url to check it does not have URL query parameters
        self.url = url
        self.description = description
        # TODO: validate url against declared variables
        self.variables = variables
