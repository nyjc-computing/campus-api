"""campus/wrapper

A Campus Web API wrapper for Python.

The API for operations follows the Campus API specification, with resources
represented as attribute, ids represented as dictionary keys, and operations
represented as methods.
"""

from campus.api.api import CampusClient

__all__ = [
    "CampusClient",
]
