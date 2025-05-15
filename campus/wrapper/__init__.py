"""campus/wrapper

Encapsulates operations on Campus resources.

The API for operations follows the Campus API specification.
Campus resources are represented through the CampusClient class, with
each resource represented as an attribute.
"""

from typing import Literal

from campus.operations import ClientCollection, UserCollection

Version = Literal["v1"]


class CampusClient:
    clients: ClientCollection
    users: UserCollection

    def __init__(self, base_url: str, version: Version = Literal["v1"]):
        self.base_url = base_url
        # TODO: Add authentication parameters
        self.clients = ClientCollection(self)
        self.users = UserCollection(self)
