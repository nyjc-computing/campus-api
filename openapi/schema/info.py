"""openapi/info

Classes for representing API info
"""

from typing import Mapping, Sequence

Email = str
Url = str


class ContactInfo:
    """Represents server admin contact info as defined in OpenAPI 3.0.
    https://swagger.io/docs/specification/v3_0/api-general-info/
    """
    name: str | None
    email: Email | None
    url: Url | None

    def __init__(
            self,
            name: str | None = None,
            email: Email | None = None,
            url: Url | None = None
    ):
        self.name = name
        self.email = email
        self.url = url


class LicenseInfo:
    """Represents server license info as defined in OpenAPI 3.0.
    https://swagger.io/docs/specification/v3_0/api-general-info/
    """
    name: str | None
    url: Url | None

    def __init__(
            self,
            name: str | None = None,
            url: Url | None = None
    ):
        self.name = name
        self.url = url


class ExternalDocs:
    """Represents external documentation as defined in OpenAPI 3.0.
    https://swagger.io/docs/specification/v3_0/api-general-info/
    """
    description: str | None
    url: Url | None

    def __init__(
            self,
            description: str | None = None,
            url: Url | None = None
    ):
        self.description = description
        self.url = url


class Info:
    """Represents API info as defined in OpenAPI 3.0.
     https://swagger.io/docs/specification/v3_0/api-general-info/
    """
    title: str
    version: str
    description: str | None = None
    termsOfService: Url | None = None
    contact: ContactInfo | None = None
    license: LicenseInfo | None = None

    def __init__(
            self,
            title: str,
            version: str,
            description: str | None = None,
            termsOfService: Url | None = None,
            externalDocs: ExternalDocs | None = None
    ):
        self.title = title
        self.version = version
        self.description = description
        self.termsOfService = termsOfService
