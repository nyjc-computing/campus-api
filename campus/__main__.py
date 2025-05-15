"""campus.py

Main entry point for the campus module."""

import sys

from campus.cli import Parser


if __name__ == "__main__":
    parser = Parser(sys.argv)
    apiresult = parser.parse()
    if apiresult:
        result = apiresult.give()
        # TODO: Format result
        print(result)
    sys.exit(0)
