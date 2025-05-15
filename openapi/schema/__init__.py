"""openapi/schema

This module contains classes for representing the OpenAPI schema only.
These classes are used to define the structure of the API and its components.
They are used as intermediate representations for converting to and from the
OpenAPI format.

Note that OpenAPI 3.0 does not have an explicit null type as in JSON Schema,
so None is used to represent an unused property.
"""
from .components import Components
from .datatypes import (
    Schema,
    String,
    Number,
    Integer,
    Boolean,
    Array,
    Object,
    Byte,
    Date,
    DateTime,
    Email,
    Time,
    AllOf,
    AnyOf,
    OneOf,
)
from .info import (
    ContactInfo,
    LicenseInfo,
    ExternalDocs,
    Info
)
from .paths import (
    GetOperation,
    PostOperation,
    PutOperation,
    DeleteOperation,
    PatchOperation,
    HeadOperation,
    OptionsOperation,
    TraceOperation,
    ConnectOperation,
    Parameter,
    Path,
)
from .reference import (
    PathReference,
    SchemaReference,
)
from .request import RequestBody
from .response import Response
from .server import Server


__all__ = [
    "Components",
    "Schema",
    "String",
    "Number",
    "Integer",
    "Boolean",
    "Array",
    "Object",
    "Byte",
    "Date",
    "DateTime",
    "Email",
    "Time",
    "AllOf",
    "AnyOf",
    "OneOf",
    "ContactInfo",
    "LicenseInfo",
    "ExternalDocs",
    "Info",
    "GetOperation",
    "PostOperation",
    "PutOperation",
    "DeleteOperation",
    "PatchOperation",
    "HeadOperation",
    "OptionsOperation",
    "TraceOperation",
    "ConnectOperation",
    "Parameter",
    "Path",
    "PathReference",
    "SchemaReference",
    "RequestBody",
    "Response",
    "Server",
]
