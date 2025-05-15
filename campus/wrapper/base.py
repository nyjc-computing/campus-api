from campus.schema.datatypes import UserID, CampusID


class CampusAPI:
    """A typing stub for the Campus API Client."""

class CampusResource:
    """Base class for resources in the Campus API.

    This class provides a common interface for all resources.
    """

    def __init__(self, parent: "CampusResource" | CampusAPI):
        self.parent = parent

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


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
