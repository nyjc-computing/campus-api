"""campus - A Python wrapper for the Campus API."""

from .api import CampusClient, get_client


__all__ = [
    "CampusClient",
    "get_client",
]
