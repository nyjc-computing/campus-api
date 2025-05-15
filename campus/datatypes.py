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
UserIDPattern = r'[a-zA-Z0-9._-]{1,64}'
DomainPattern = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
EmailAddress = fr'{UserID}@{Domain}'

Uid8Pattern = fr'{LowerLetterDecimalChar}{{8}}'
Uid16Pattern = fr'{LowerLetterDecimalChar}{{16}}'

UidPrefix = Literal["uid"]


class StringPattern(str):
    """String pattern is a string with a regex pattern.

    The pattern is used to validate the string.
    """
    pattern: re.Pattern

    def __new__(cls, value):
        """Validation is not carried out at instantiation time."""
        return super().__new__(cls, value)
    
    @classmethod
    def validate(cls, value: str) -> None:
        """Validate the string value against the pattern.
        
        This method is defined as a class method, so it can be called
        within __new__ if necessary.
        """
        if not cls.pattern.match(value):
            raise ValueError(
                f"Value does not match pattern {cls.pattern.pattern!r}: {value}"
            )


class UserID(StringPattern):
    """User IDs are the username part of the email address, for simplicity."""
    pattern = fr'^{UserIDPattern}$'


class Domain(StringPattern):
    """Domain names are the domain part of the email address."""
    pattern = fr'^{DomainPattern}$'


class EmailAddress(StringPattern):
    """A typical email address."""
    pattern = fr'^{UserIDPattern}@{DomainPattern}$'

    def __new__(cls, value):
        cls.validate(value)  # Ensure valid email address first
        string = super().__new__(cls, value)
        _user_id, _domain = value.split('@')
        string.user_id = UserID(_user_id)
        string.domain = Domain(_domain)
        return string


class UID(StringPattern):
    """Campus IDs are based on shortened, base64-encoded UUIDs.

    They only use lowercase letters and numbers for ease of use.

    Campus IDs are 8 or 16 characters.
    - 8 chars are used for resource IDs, expected to be limited in number.
    - 16 chars are used for source IDs, event IDs and other voluminuous IDs.
    """
    pattern: re.Pattern


class CampusID(UID):
    """Campus IDs are UIDs UidPrefixed with a namespace.

    The namespace is 'uid-' followed by a string of hyphenated lowercase words,
      with up to 3 parts.

    Example: uid-client-12345678
    """
    pattern = fr"^{UidPrefix}-({CampusLabel})-({Uid8Pattern})$"

    def __new__(cls, value):
        if not (match := cls.pattern.match(value)):
            raise ValueError(
                f"Value does not match pattern {cls.pattern.pattern!r}: {value}"
            )
        string = super().__new__(cls, value)
        _label, _uid = match.groups()
        string.label = CampusLabel(_label)
        string.uid = UID(_uid)
        return string


class ClientID(CampusID):
    """Client IDs are UIDs UidPrefixed with a namespace.

    The namespace is 'uid-client-' followed by a string of lowercase letters
      and numbers, with a length of 8 characters.

    Example: uid-client-12345678
    """
    pattern = fr"^{UidPrefix}-client-{Uid8Pattern}$"
    label: Literal["client"]


class CircleID(CampusID):
    """Circle IDs are UIDs UidPrefixed with a namespace.

    The namespace is 'uid-circle-' followed by a string of lowercase letters
      and numbers, with a length of 8 characters.

    Example: uid-circle-12345678
    """
    pattern = fr"^{UidPrefix}-circle-{Uid8Pattern}$"
    label: Literal["circle"]


class OTP(StringPattern):
    """One-time password (OTP) is a 6-digit number.

    Example: 123456
    """
    pattern = fr"^{DecimalChar}{{6}}$"
