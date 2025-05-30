"""openapi/paths

Classes for representing API paths
"""

from typing import Literal, Mapping, Sequence, get_args

from .datatypes import Content, Schema
from .info import ExternalDocs
from .request import RequestBody
from .response import Response
from .server import Server

PathPattern = str
HttpMethod = Literal["get", "post", "patch", "put", "delete", "head", "options", "trace", "connect"]
ParameterLocation = Literal["cookie", "header", "path", "query"]


class Parameter:
    """Represents an operation as defined in OpenAPI 3.0.

    Note that this implementation of OpenAPI 3.0 schema does not
    support array and object parameters.

    https://swagger.io/docs/specification/v3.0/paths-and-operations/
    """
    in_: ParameterLocation
    name: str
    summary: str | None = None
    description: str | None
    schema: Schema | None
    content: Content | None
    required: bool | None

    def __init__(
            self,
            in_: ParameterLocation,
            name: str,
            summary: str | None = None,
            description: str | None = None,
            schema: Schema | None = None,
            content: Content | None = None,
            required: bool | None = None,
    ):
        if schema and content:
            raise ValueError("Specify schema or content, not both")
        if in_ == "path" and not required:
            raise ValueError("Path parameters must have `required: true`")
        if schema.default is not None and required:
            raise ValueError("Schema default value will never be used as parameter value is required")
        if content:
            raise NotImplementedError("This version of the OpenAPI 3.0 spec does not support `content` parameters yet.")
        self.in_ = in_
        self.name = name
        self.summary = summary
        self.description = description
        self.schema = schema
        self.content = content
        self.required = required


class Operation:
    """Represents an operation as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3.0/paths-and-operations/
    """
    method: HttpMethod
    deprecated: bool | None
    requestBody: RequestBody | None
    responses: Sequence[Response] | None 
    operationId: str | None
    tags: Sequence[str]
    summary: str | None
    description: str | None
    parameters: Sequence[Parameter] | None
    externalDocs: ExternalDocs | None
    servers: Sequence[Server] | None

    def __init__(
            self,
            *,
            deprecated: bool | None = None,
            requestBody: RequestBody | None = None,
            responses: Sequence[Response] | None = None, 
            operationId: str | None = None,
            tags: Sequence[str] = (),
            summary: str | None = None,
            description: str | None = None,
            parameters: Sequence[Parameter] | None = None,
            externalDocs: ExternalDocs | None = None,
            servers: Sequence[Server] | None = None,
    ):
        self.deprecated = deprecated
        self.requestBody = requestBody
        self.responses = responses
        self.operationId = operationId
        self.tags = tuple(tags)
        self.summary = summary
        self.description = description
        self.parameters = parameters
        self.externalDocs = externalDocs
        self.servers = servers
        
    
class GetOperation(Operation):
    method: HttpMethod = "get"

class PostOperation(Operation):
    method: HttpMethod = "post"

class PutOperation(Operation):
    method: HttpMethod = "put"

class DeleteOperation(Operation):
    method: HttpMethod = "delete"

class PatchOperation(Operation):
    method: HttpMethod = "patch"

class HeadOperation(Operation):
    method: HttpMethod = "head"

class OptionsOperation(Operation):
    method: HttpMethod = "options"

class TraceOperation(Operation):
    method: HttpMethod = "trace"

class ConnectOperation(Operation):
    method: HttpMethod = "connect" 


class Path:
    """Represents an API endpoint path as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3.0/paths-and-operations/
    """
    path: PathPattern
    summary: str | None = None
    description: str | None = None
    methods: Mapping[HttpMethod, Operation]

    def __init__(
            self,
            path: PathPattern,
            summary: str | None = None,
            description: str | None = None,
            **methods: Operation
    ):
        self.path = path
        self.summary = summary
        self.description = description
        invalid_methods = [
            method for method in methods
            if methods not in get_args(HttpMethod)
        ]
        if invalid_methods:
            raise KeyError(f"Invalid HTTP method: {invalid_methods}")
        self.methods = methods
