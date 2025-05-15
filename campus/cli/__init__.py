"""campus/cli

Command line interface for the Campus API.
"""
import logging
import os
import sys
from typing import Callable, Mapping, Sequence
from warnings import warn

from campus.api import CampusClient, CampusResource, get_client
from campus.cli import pattern

logging.basicConfig(level=logging.INFO)

__version__ = "0.1.0"

HELP_DIR = os.path.dirname(__file__)
HELP_FILE = "README.md"
SEP = " "

client = get_client()


class ParseError(Exception):
    """Custom exception for parse errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        logging.error(f"ParseError: {message}")


class APICall:
    """Encapsulates an API call."""

    def __init__(
            self,
            resource,
            params: Mapping,
            *,
            path: list[str],
    ):
        self.resource = resource
        self.params = params

    def give(self):
        """Return the API call result."""
        if isinstance(self.resource, Callable):
            return self.resource(**self.params)
        elif isinstance(self.resource, dict):
            return self.resource
        raise TypeError(f"{self.resource}: Resource is not callable or dict.")


class Parser:
    """A simple command line parser."""

    def __init__(self, args: Sequence[str]):
        self.args = args
        # Number of arguments
        self.arglen = len(args)
        # Index of next argument to consume
        self.pos = 0
        # List of consumed arguments
        self.consumed = []

    def atEnd(self) -> bool:
        """Check if the end of the arguments is reached."""
        return self.pos >= self.arglen

    def consume(self) -> str:
        """Consume the next argument."""
        if self.pos >= self.arglen:
            raise ParseError("Incomplete command.")
        arg = self.args[self.pos]
        self.pos += 1
        self.consumed.append(arg)
        return arg
    
    def current_resource(self) -> str:
        """Get the current resource path."""
        return " ".join(self.consumed)

    def help(self) -> None:
        """Display help information."""
        with open(os.path.join(HELP_DIR, HELP_FILE), 'r') as f:
            print(f.read())

    def version(self) -> None:
        """Display version information."""
        print(f"Campus CLI version {__version__}")
        print(f"Campus API version {client.version}")

    def parse(self) -> APICall | None:
        """Parse the command line arguments."""
        program = self.consume()
        # if program != "campus":
        #     warn(f"Unexpected programe name: {program}", UserWarning, 2)
        resource = client  # type: ignore
        params = {}
        while not self.atEnd():
            arg = self.consume()
            # 1st argument is program name, 2nd argument is arg
            if self.pos == 2:
                # Special handling for `help` and `version`
                if arg == 'help':
                    self.help()
                elif arg == 'version':
                    self.version()

            if pattern.is_resource_name(arg):
                # Check if the resource exists
                if not hasattr(resource, arg):
                    raise ParseError(f"Unknown resource: {arg}")
                resource: CampusResource = getattr(resource, arg)

            elif pattern.is_campus_id(arg):
                # Check if resource supports [] operation
                if not hasattr(resource, "__getitem__"):
                    raise ParseError(f"Unexpected campus ID: {arg}")
                resource = resource[arg]  # type: ignore

            elif pattern.is_campus_verb(arg):
                # Check if the resource has a method for this verb
                if not hasattr(resource, arg):
                    raise ParseError(f"Unexpected verb: {arg}")
                resource = getattr(resource, arg)

            elif pattern.is_param_pair(arg):
                key, value = arg.split("=")
                # TODO: value conversion
                params[key] = value
            try:
                resource = getattr(resource, arg)
            except AttributeError as err:
                raise ParseError(f"Unknown resource: {arg}") from err
        return APICall(resource, params, path=self.consumed)
