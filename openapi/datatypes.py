"""openapi.datatypes

Data types as defined in the OpenAPI 3.0 Specification.
https://swagger.io/docs/specification/v3_0/data-models/data-types/
"""
from abc import ABC, abstractmethod
from typing import Literal

BasicType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "array",
    "object"
]

class Schema(ABC):
    """Base class for all schemas."""

    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"
    
    def to_dict(self) -> dict:
        """Convert the schema to a json dictionary."""
        raise NotImplementedError("Subclasses must implement to_dict() method.")
    
class BasicSchema(Schema):
    """Base class for basic schemas."""
    type: BasicType

    def __init__(self, value: BasicType):
        super().__init__(value)

    def to_dict(self) -> dict:
        if hasattr(self, "format") and self.format is not None:
            return {"type": self.type, "format": self.format}
        else:
            return {"type": self.type}

class String(Schema):
    type: BasicType = "string"
    format: str | None = None

class Number:
    type: BasicType = "number"
    format: str | None = None

class Integer:
    type: BasicType = "integer"
    format: str | None = None

class Boolean:
    type: BasicType = "boolean"

class Array:
    type: BasicType = "array"

class Object:
    type: BasicType = "object"
