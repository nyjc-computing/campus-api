"""openapi.datatypes

Data types as defined in the OpenAPI 3.0 Specification.
https://swagger.io/docs/specification/v3_0/data-models/data-types/
"""
from abc import ABC, abstractmethod
from typing import Any, Literal, Mapping

from .reference import SchemaReference

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


def format_sequence(
        sequence: list[Any],
        separator: str = ", ",
        start: str = "(",
        end: str = ")",
) -> str:
    """Format a sequence as a string.

    Args:
        sequence: A sequence of items.

    Returns:
        A string representation of the sequence.
    """
    return f"{start}{separator.join(map(repr, sequence))}{end}"


def format_keyvalues(
        keyvalues: dict[str, Any],
        delimiter: str = "=",
        separator: str = ", ",
        start: str = "(",
        end: str = ")",
) -> str:
    """Format a dictionary of key-value pairs as a string.

    Args:
        keyvalues: A dictionary of key-value pairs.

    Returns:
        A string representation of the key-value pairs.
    """
    return (
        f"{start}{separator.join(
            f"{key}{delimiter}{value!r}"
            for key, value in keyvalues.items()
        )}{end}"
    )


class Schema(ABC):
    """Base class for all schemas.

    All schemas must inherit from this class.
    """

    @abstractmethod
    def to_json(self) -> dict:
        """Convert the schema to a json dictionary."""
        pass



# Basic types

class BasicSchema(Schema):
    """Base class for basic schemas."""
    # type should be declared as a class variable
    nullable: bool | None = None
    type: BasicType

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"

    def to_json(self) -> dict:
        if hasattr(self, "format") and self.format is not None:
            return {"type": self.type, "format": self.format}
        else:
            return {"type": self.type}


class FormatSchema(Schema):
    """Base class for schemas with (optional) format."""
    type: BasicType
    format: str | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"

    def to_json(self) -> dict:
        json_ = {"type": self.type}
        if self.format is not None:
            json_["format"] = self.format
        return json_


class String(FormatSchema):
    type: BasicType = "string"
    format: str | None = None
    pattern: str | None = None
    enum: list[Schema | SchemaReference] | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"

    def to_json(self) -> dict:
        result = super().to_json()
        if self.enum is not None:
            result["enum"] = [enum.to_json() for enum in self.enum]
        if self.pattern is not None:
            result["pattern"] = self.pattern
        return result


class Number(FormatSchema):
    type: BasicType = "number"
    format: str | None = None
    enum: list[float | int] | None = None

    def to_json(self) -> dict:
        result = super().to_json()
        if self.enum is not None:
            result["enum"] = [enum.to_json() for enum in self.enum]
        return result


class Integer(BasicSchema):
    type: BasicType = "integer"
    format: str | None = None
    enum: list[int] | None = None

    def to_json(self) -> dict:
        result = super().to_json()
        if self.enum is not None:
            result["enum"] = [enum.to_json() for enum in self.enum]
        return result


class Boolean(BasicSchema):
    type: BasicType = "boolean"


class Array(Schema):
    type: BasicType = "array"
    items: Schema | SchemaReference
    minItems: int | None = None
    maxItems: int | None = None
    uniqueItems: bool | None

    def __init__(
            self,
            items: Schema | SchemaReference,
            minItems: int | None = None,
            maxItems: int | None = None,
            uniqueItems: bool | None = None
    ):
        self.items = items
        self.minItems = minItems
        self.maxItems = maxItems
        self.uniqueItems = uniqueItems
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"
    
    def to_json(self) -> dict:
        json_ = {"type": self.type, "items": self.items.to_json()}
        if self.minItems is not None:
            json_["minItems"] = self.minItems
        if self.maxItems is not None:
            json_["maxItems"] = self.maxItems
        if self.uniqueItems is not None:
            json_["uniqueItems"] = self.uniqueItems
        return json_


class Object(Schema):
    type: BasicType = "object"
    properties: dict[str, Schema | SchemaReference]
    # The readOnly and writeOnly properties are defined per property
    # For ease of use, we store them in separate mappings from properties
    readOnly: dict[str, bool]
    writeOnly: dict[str, bool]
    # Required is an object-level attribute, not a property attribute
    required: list[str] | None = None
    additionalProperties: bool | Schema | SchemaReference | None = None
    minProperties: int | None = None
    maxProperties: int | None = None

    def __init__(
            self,
            properties: dict[str, Schema | SchemaReference],
            required: list[str] | None = None,
            readOnly: list[str] | None = None,
            writeOnly: list[str] | None = None,
            additionalProperties: bool | Schema | SchemaReference | None = None,
            minProperties: int | None = None,
            maxProperties: int | None = None
    ):
        self.properties = properties
        self.required = required
        self.readOnly: dict[str, bool] = {}
        for prop in readOnly:
            if prop not in properties:
                raise ValueError(f"Property {prop!r} not defined in properties")
            self.readOnly[prop] = True
        self.writeOnly: dict[str, bool] = {}
        for prop in writeOnly:
            if prop not in properties:
                raise ValueError(f"Property {prop!r} not defined in properties")
            self.writeOnly[prop] = True
        self.additionalProperties = additionalProperties
        self.minProperties = minProperties
        self.maxProperties = maxProperties

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"
    
    def to_json(self) -> dict:
        json_ = {
            "type": self.type,
            "properties": {
                key: value.to_json()
                for key, value in self.properties.items()
            }
        }
        for prop, schema in json_.items():
            if self.readOnly.get(prop):
                schema["readOnly"] = True
            if self.writeOnly.get(prop):
                schema["writeOnly"] = True
        if self.required is not None:
            json_["required"] = self.required
        if self.readOnly is not None:
            json_["readOnly"] = self.readOnly
        if self.writeOnly is not None:
            json_["writeOnly"] = self.writeOnly
        if self.additionalProperties is not None:
            json_["additionalProperties"] = (
                self.additionalProperties.to_json()
                if isinstance(self.additionalProperties, Schema)
                else self.additionalProperties
            )
        if self.minProperties is not None:
            json_["minProperties"] = self.minProperties
        if self.maxProperties is not None:
            json_["maxProperties"] = self.maxProperties
        return json_


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



# Mixed types

class AllOf(Schema):
    """All of the given schemas.

    This is used to represent a schema that must be all of several types.
    """
    items: list[Schema]

    def __init__(self, *schemas: Schema):
        self.items = list(schemas)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_sequence(self.items)}"

    def to_json(self) -> dict:
        return {"allOf": [schema.to_json() for schema in self.items]}


class AnyOf(Schema):
    """Any of the given schemas.

    This is used to represent a schema that can be any of several types.
    """
    items: list[Schema]

    def __init__(self, *schemas: Schema):
        self.items = list(schemas)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_sequence(self.items)}"

    def to_json(self) -> dict:
        return {"anyOf": [schema.to_json() for schema in self.items]}


class OneOf(Schema):
    """One of the given schemas.

    This is used to represent a schema that can be one of several types.
    """
    items: list[Schema]

    def __init__(self, *schemas: Schema):
        self.items = list(schemas)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_sequence(self.items)}"

    def to_json(self) -> dict:
        return {"oneOf": [schema.to_json() for schema in self.items]}



# Any

class AnyValue(Schema):
    """Any value.

    This is used to represent a schema that can be any value.
    """
    description: str | None = None
    nullable: bool | None = None
    
    def __init__(
            self,
            description: str | None = None,
            nullable: bool | None = None
    ):
        self.description = description
        self.nullable = nullable
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{format_keyvalues(self.to_json())}"

    def to_json(self) -> dict:
        json_ = {}
        if self.description is not None:
            json_["description"] = self.description
        if self.nullable is not None:
            json_["nullable"] = self.nullable
        return json_
