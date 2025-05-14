"""openapi/reference

Classes for representing References
"""

from typing import Mapping, Protocol

RefPattern = str


class Reference(Protocol):
    """Represents a reference as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/using-ref/
    """
    ref: RefPattern | None

    def __init__(self, ref: RefPattern):
        # TODO: Validate RefPattern
        self.ref = ref


class PathReference(Reference):
    """A reference to a Path entry in Component."""


class SchemaReference(Reference):
    """A reference to a Schema entry in Component."""
