"""openapi/components

Classes for representing the components section of OpenAPI.
"""

class Components:
    """Represents a collection of components as defined in OpenAPI 3.0.

    https://swagger.io/docs/specification/v3_0/components/
    """
    schemas: list
    parameters: list
    securitySchemes: list
    requestBodies: list
    responses: list
    headers: list
    examples: list
    links: list
    callbacks: list
