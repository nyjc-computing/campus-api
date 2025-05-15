"""campus/wrapper/api

Encapsulates operations on Campus resources.

The API for operations follows the Campus API specification.
Campus resources are represented through the CampusClient class, with
each resource represented as an attribute.
"""

from campus.wrapper.base import CampusAPI
from campus.wrapper.clients import Clients
from campus.wrapper.users import Users


class CampusClient(CampusAPI):
    clients: Clients
    users: Users

    def __init__(self, base_url: str, version = "v1"):
        super().__init__(base_url, version)
        # TODO: Add authentication parameters
        self.clients = Clients(self)
        self.users = Users(self)
