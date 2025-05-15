"""campus/wrapper

Encapsulates operations on Campus resources.

The API for operations follows the Campus API specification.
Campus resources are represented through the CampusClient class, with
each resource represented as an attribute.
"""

from campus.operations import ClientCollection, UserCollection

class CampusClient:
    clients: ClientCollection
    users: UserCollection

    def __init__(self):
        # TODO: Add authentication parameters
        self.clients = ClientCollection(self)
        self.users = UserCollection(self)
