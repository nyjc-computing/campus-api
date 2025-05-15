"""campus/cli

Command line interface for the Campus API.
"""
import logging
import sys
from typing import Callable, Mapping, Sequence
from warnings import warn

from campus.api import get_client

logging.basicConfig(level=logging.INFO)

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
            api_callable: Callable,
            params: Mapping,
            *,
            path: list[str],
    ):
        self.callable = api_callable
        self.params = params

    def __call__(self):
        """Call the API with the given parameters."""
        logging.debug(f"API path: {self.path}")
        logging.debug(f"API params: {", ".join(
            [f'{k}={v}' for k, v in self.params.items()]
        )}")
        try:
            result = self.callable(**self.params)
            return result
        except Exception as err:
            raise ParseError(f"API call failed: {err}") from err


class Parser:
    """A simple command line parser."""

    def __init__(self, args: Sequence[str]):
        self.args = args
        self.arglen = len(args)
        self.pos = 0
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

    def parse(self) -> APICall:
        """Parse the command line arguments."""
        program = self.consume()
        if program != "campus":
            warn(f"Unexpected programe name: {program}", UserWarning, 2)
        resource = client
        params = {}
        while not self.atEnd():
            arg = self.consume()
            # TODO: Pattern-match tokens
            # - resource name
            # - campus_id
            # - verb
            # - params
            # - additional commands (e.g. help)
            try:
                resource = getattr(resource, arg)
            except AttributeError as err:
                raise ParseError(f"Unknown resource: {arg}") from err
        return APICall(resource, params, path=self.consumed)


if __name__ == "__main__":
    parser = Parser(sys.argv)
    apicall = parser.parse()
    result = apicall()
    # TODO: Format result
    print(result)
