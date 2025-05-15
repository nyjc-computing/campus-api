"""campus/api

A Campus Web API wrapper for Python.

The API for operations follows the Campus API specification, with resources
represented as attribute, ids represented as dictionary keys, and operations
represented as methods.
"""

from campus.api.api import CampusClient
from campus import config

__all__ = [
    "CampusClient",
]


def get_client(cfg: dict | None = None, **kwargs) -> CampusClient:
    """Get a CampusClient instance."""
    cfg = cfg or config.default.copy()
    cfg.update(kwargs)
    return CampusClient.from_config(cfg)
