"""campus.config

Configuration management for the Campus API Python wrapper.
"""
import os

from .utils import load_config

DEFAULT_CONFIG_FILE = 'default.json'
DEFAULT_CONFIG_DIR = os.path.dirname(__file__)

default = load_config(os.path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE))
