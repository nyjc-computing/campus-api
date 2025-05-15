"""campus/operations

Represents operations on Campus resources.

The API for operations follows the Campus API specification, with resources
represented as attribute, ids represented as dictionary keys, and operations
represented as methods.
"""

from campus.wrapper.api import CampusClient

__all__ = [
    "CampusClient",
]
