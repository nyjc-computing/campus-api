"""openapi/reference

Classes for representing References
"""

from typing import Protocol

from openapi.schema.datatypes import Schema

RefPattern = str


class Reference(Schema):
    """Represents a reference as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/using-ref/
    """
    ref: RefPattern

    def __init__(self, ref: RefPattern):
        # TODO: Validate RefPattern
        self.ref = ref

    def to_json(self) -> dict:
        return {"$ref": self.ref}


class PathReference(Reference):
    """A reference to a Path entry in Component."""


class SchemaReference(Reference):
    """A reference to a Schema entry in Component."""
