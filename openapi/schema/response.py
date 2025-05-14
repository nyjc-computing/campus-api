"""openapi/paths

Classes for representing API paths
"""

from .datatypes import Content


class Response:
    """Represents a response as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3.0/describing-responses/
    """
    status_code: str  # OpenAPI represents status codes as strings
    description: str | None
    content: Content

    def __init__(
            self,
            status_code: str,
            content: Content,
            description: str | None = None,
    ):
        self.status_code = status_code
        self.description = description
        self.content = dict(content)
