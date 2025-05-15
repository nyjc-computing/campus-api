"""campus/datatypes

Campus data types, designed for OpenAPI compatibility.
The data types are based on native Python types as far as possible,
and will be used to generate OpenAPI schemas for the campus API.
"""
import re
from typing import Literal

# Lowercase letters only
LowerLetterChar = r'[a-z]'
DecimalChar = r'[0-9]'
# Lowercase letters and numbers
LowerLetterDecimalChar = r'[a-z0-9]'
# Lowercase word (limit length to 15 characters, disallow single character)
LowerLetterWord = r'[a-z]{2,15}'

# Resource names are limited to a single lowercase word
ResourceName = LowerLetterWord
# Campus allows hyphenated lowercase words (up to 3 parts) as name labels
CampusLabel = fr'{LowerLetterWord}(-{LowerLetterWord}){{0,2}}'
UserID = r'[a-zA-Z0-9._-]{1,64}'
Domain = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
EmailAddress = fr'{UserID}@{Domain}'

Uid8Pattern = fr'{LowerLetterDecimalChar}{{8}}'
Uid16Pattern = fr'{LowerLetterDecimalChar}{{16}}'

Prefix = Literal["uid"]


class StringPattern(str):
    """String pattern is a string with a regex pattern.

    The pattern is used to validate the string.
    """
    pattern: re.Pattern

    def __new__(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid string: {value}")
        return super().__new__(cls, value)


class UID(StringPattern):
    """Campus IDs are based on shortened, base64-encoded UUIDs.

    They only use lowercase letters and numbers for ease of use.

    Campus IDs are 8 or 16 characters.
    - 8 chars are used for resource IDs, expected to be limited in number.
    - 16 chars are used for source IDs, event IDs and other voluminuous IDs.
    """
    pattern: re.Pattern

    def __new__(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid UID: {value}")
        return super().__new__(cls, value)


class CampusID(UID):
    """Campus IDs are UIDs prefixed with a namespace.

    The namespace is 'uid-' followed by a string of hyphenated lowercase words,
      with up to 3 parts.

    Example: uid-client-12345678
    """
    pattern = fr"^{Prefix}-{CampusName}-{Uid8Pattern}$"

    def __new__(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid UID: {value}")
        return super().__new__(cls, value)


class ClientID(UID):
    """Client IDs are UIDs prefixed with a namespace.

    The namespace is 'uid-client-' followed by a string of lowercase letters
      and numbers, with a length of 8 characters.

    Example: uid-client-12345678
    """
    pattern = fr"^{Prefix}-client-{Uid8Pattern}$"

    def __new__(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid UID: {value}")
        return super().__new__(cls, value)


class CircleID(UID):
    """Circle IDs are UIDs prefixed with a namespace.

    The namespace is 'uid-circle-' followed by a string of lowercase letters
      and numbers, with a length of 8 characters.

    Example: uid-circle-12345678
    """
    pattern = fr"^{Prefix}-circle-{Uid8Pattern}$"

    def __new__(cls, value):
        if not cls.pattern.match(value):
            raise ValueError(f"Invalid UID: {value}")
        return super().__new__(cls, value)


class OTP(StringPattern):
    """One-time password (OTP) is a 6-digit number.

    Example: 123456
    """
    pattern = fr"^{DecimalChar}{{6}}$"
