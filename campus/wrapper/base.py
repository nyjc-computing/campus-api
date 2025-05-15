import re
from typing import Protocol

from campus.schema.datatypes import UserID, CampusID

# OpenAPI does not support null values, only nullable types
JsonSerializableValues = int | float | str | bool
JsonSerializable = JsonSerializableValues | list["JsonSerializable"] | dict[str, "JsonSerializable"]

BaseUrlPattern = re.compile(
    r"^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$"
)
VersionPattern = re.compile(r"^v\d+$")

URL_SEP = "/"


class BaseUrl(str):
    """A class representing a base URL.

    This class is used to validate and represent a base URL.
    """

    def __new__(cls, value: str):
        if not BaseUrlPattern.match(value):
            raise ValueError(f"Invalid base URL: {value}")
        return super().__new__(cls, value)

class Version(str):
    """A class representing a version.

    This class is used to validate and represent a version.
    """

    def __new__(cls, value: str):
        if not VersionPattern.match(value):
            raise ValueError(f"Invalid version: {value}")
        return super().__new__(cls, value)


class Pathable(Protocol):
    """A protocol for objects that can be converted to a path.

    This protocol is used to define the interface for objects that can
    be converted to a path.
    """

    def build_path(self, *args, **kwargs) -> str:
        """Convert the object to a string."""
        pass


class CampusAPI(Pathable):
    """A typing stub for the Campus API Client."""
    base_url: BaseUrl
    version: Version

    def __init__(self, base_url: str, version: str, *args, **kwargs):
        self.base_url = BaseUrl(base_url)
        self.version = Version(version)
        
    def build_path(self, *args: str) -> str:
        """Build a path for the API.

        This method is used to build a path for the API call.
        """
        return URL_SEP.join([self.base_url, self.version, *args])

class CampusResource(Pathable):
    """Base class for resources in the Campus API.

    This class provides a common interface for all resources.
    """

    def __init__(self, parent: "CampusAPI | CampusResource"):
        self.parent = parent

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
    
    def build_path(self, *args: str) -> str:
        """Build a path for the resource.

        This method is used to build a path for the resource.
        """
        return "/".join([self.parent.build_path, *args])


class SingleResource(CampusResource):
    """Base class for single resources in the Campus API.

    This class provides a common interface for all single resources,
    including methods for creating, updating, and deleting resources.
    """

    def __init__(self, parent: CampusResource, id: CampusID | UserID):
        super().__init__(parent)
        self.id = id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"


class ResourceCollection(CampusResource):
    """Base class for resource collections in the Campus API.

    This class provides a common interface for all resources, including
    methods for creating, updating, and deleting resources.
    """
