"""campus/wrapper/api

Encapsulates operations on Campus resources.

The API for operations follows the Campus API specification.
Campus resources are represented through the CampusClient class, with
each resource represented as an attribute.
"""

from typing import Literal

from campus.wrapper.base import CampusAPI
from campus.wrapper.clients import Clients
from campus.wrapper.users import Users

Version = Literal["v1"]


class CampusClient(CampusAPI):
    clients: Clients
    users: Users

    def __init__(self, base_url: str, version: Version = Literal["v1"]):
        self.base_url = base_url
        # TODO: Add authentication parameters
        self.clients = Clients(self)
        self.users = Users(self)
