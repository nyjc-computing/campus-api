"""campus - A Python wrapper for the Campus API."""

from .api import CampusClient
from . import config


def get_client(cfg: dict | None = None, **kwargs) -> CampusClient:
    """Get a CampusClient instance."""
    cfg = cfg or config.default.copy()
    cfg.update(kwargs)
    return CampusClient.from_config(cfg)

__all__ = [
    "CampusClient",
]
