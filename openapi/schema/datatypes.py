"""openapi.datatypes

Data types as defined in the OpenAPI 3.0 Specification.
https://swagger.io/docs/specification/v3_0/data-models/data-types/
"""
from abc import ABC, abstractmethod
from typing import Literal, Mapping

Mimetype = str
Content = Mapping[Mimetype, "Schema"]

BasicType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
    "array",
    "object"
]



class Schema(ABC):
    """Base class for all schemas.

    All schemas must inherit from this class.
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"
    
    @abstractmethod
    def to_json(self) -> dict:
        """Convert the schema to a json dictionary."""
        pass



# Basic types

class BasicSchema(Schema):
    """Base class for basic schemas."""
    # type should be declared as a class variable
    type: BasicType

    def __init__(self, value: BasicType):
        super().__init__(value)

    def to_json(self) -> dict:
        if hasattr(self, "format") and self.format is not None:
            return {"type": self.type, "format": self.format}
        else:
            return {"type": self.type}


class String(BasicSchema):
    type: BasicType = "string"
    format: str | None = None
    pattern: str | None = None


class Number(BasicSchema):
    type: BasicType = "number"
    format: str | None = None


class Integer(BasicSchema):
    type: BasicType = "integer"
    format: str | None = None


class Boolean(BasicSchema):
    type: BasicType = "boolean"


class Array(Schema):
    type: BasicType = "array"
    
    # TODO


class Object(Schema):
    type: BasicType = "object"

    # TODO



# String formats

class Byte(String):
    """Base64 encoded string.

    Example: "SGVsbG8gV29ybGQh"
    """
    type: BasicType = "string"
    format: str = "byte"


class Date(String):
    """Date format as defined in RFC 3339, section 5.6.

    Example: "2023-10-01"
    """
    type: BasicType = "string"
    format: str = "date"


class DateTime(String):
    """Date-time format as defined in RFC 3339, section 5.6.

    Example: "2023-10-01T12:00:00Z
    """
    type: BasicType = "string"
    format: str = "date-time"


class Email(String):
    """Email format as defined in RFC 5322.

    Example: user.name_2024@nyjc.edu.sg
    """
    type: BasicType = "string"
    format: str = "email"


class Time(String):
    """Time format as defined in RFC 3339, section 5.6.

    Example: "12:00:00Z"
    """
    type: BasicType = "string"
    format: str = "time"
