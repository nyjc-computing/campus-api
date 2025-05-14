"""openapi/request

Classes for representing Requests
"""

from typing import Mapping

Mimetype: str
Content: Mapping[Mimetype, Schema]


class RequestBody:
    """Represents a request body as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3.0/describing-request-body/
    """
    description: str | None
    required: bool | None
    content: Content

    def __init__(
            self,
            content: Content
            description: str | None = None,
            required: bool | None = None,
    ):
        self.required = required
        self.description = description
        self.content = dict(content)