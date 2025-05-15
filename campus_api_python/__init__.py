"""campus_api_python - A Python wrapper for the Campus API."""

from .wrapper import CampusClient

from .utils import load_config

default_config = load_config("config.json")

def get_client(config: dict | None = default_config, **kwargs) -> CampusClient:
    """Get a CampusClient instance."""
    config = config.copy().update(kwargs)
    return CampusClient.from_config(config)

__all__ = [
    "CampusClient",
]
