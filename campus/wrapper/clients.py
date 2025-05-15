"""campus/operations/clients

Represents operations on the clients resource in Campus.
"""

from campus.schema.datatypes import ClientID, Validatable
from campus.schema.modeltypes import Client
from campus.wrapper.base import SingleResource, ResourceCollection


class Client(SingleResource):
    """Represents operations on a single client resource in Campus."""

    def __init__(self, parent, id: ClientID):
        super().__init__(parent)
        self.id = id


class Clients(ResourceCollection):
    """Represents operations on clients in Campus."""

