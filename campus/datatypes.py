"""campus/datatypes

Campus data types, designed for OpenAPI compatibility.
The data types are based on native Python types as far as possible,
and will be used to generate OpenAPI schemas for the campus API.
"""
from datetime import date, datetime, time
import re
from typing import Any, Literal, Protocol, runtime_checkable

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
CampusLabelPattern = fr'{LowerLetterWord}(-{LowerLetterWord}){{0,2}}'
UserIDPattern = r'[a-zA-Z0-9._-]{1,64}'
DomainPattern = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

Uid8Pattern = fr'{LowerLetterDecimalChar}{{8}}'
Uid16Pattern = fr'{LowerLetterDecimalChar}{{16}}'

# Date and time patterns as defined in RFC 3339, section 5.6 (from OpenAPI 3.0)
YearPattern = r'\d{4}'
MonthPattern = r'0[1-9]|1[0-2]'
DayPattern = r'0[1-9]|[12][0-9]|3[01]'
DatePattern = fr'{YearPattern}-{MonthPattern}-{DayPattern}'
HourPattern = r'0[0-9]|1[0-9]|2[0-3]'
MinutePattern = r'[0-5][0-9]'
SecondPattern = r'[0-5][0-9]'
TimePattern = fr'{HourPattern}:{MinutePattern}:{SecondPattern}'
DatetimePattern = fr'{DatePattern}T{TimePattern}Z'

UidPrefix = Literal["uid"]


@runtime_checkable
class Validatable(Protocol):
    """Base class for all values requiring validation."""

    def validate(self, value: Any) -> None:
        """Validate the value against the pattern, raising a ValueError if
        invalid.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement validate()"
        )

class String(Validatable, str):
    """A typical string type."""
    
    @classmethod
    def validate(cls, value: str) -> None:
        """Validate the string value."""
        if not isinstance(value, str):
            raise ValueError(f"Value is not a string: {value}")


class StringPattern(Validatable, str):
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
    pattern = fr"^{UidPrefix}-({CampusLabelPattern})-({Uid8Pattern})$"

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


class CampusLabel(StringPattern):
    """Campus labels are hyphenated lowercase words.

    The label is limited to 3 parts, and each part is a lowercase word
    with a length of 2 to 15 characters.
    """
    pattern = fr"^{CampusLabelPattern}$"


class OTP(StringPattern):
    """One-time password (OTP) is a 6-digit number.

    Example: 123456
    """
    pattern = fr"^{DecimalChar}{{6}}$"


class Date(StringPattern):
    """Date is a string in the format YYYY-MM-DD.

    Example: 2023-10-01

    This class mimics the datetime.date class, and provides a date property
    """
    pattern = fr"^{DatePattern}$"

    def __new__(cls, value):
        string = super().__new__(cls, value)
        string.year = int(value[:4])
        string.month = int(value[5:7])
        string.day = int(value[8:10])
        string.date = datetime.strptime(value, "%Y-%m-%d").date()

    def replace(self, **kwargs) -> "Date":
        """Return a new Date with the same values, but with specified
        parameters updated.
        """
        new_date = datetime.strptime(self, "%Y-%m-%d").date().replace(**kwargs)
        return Date(new_date.strftime("%Y-%m-%d"))
    
    def weekday(self) -> int:
        """Return the weekday of the date (0=Monday, 6=Sunday)."""
        return self.date.weekday()
    
    def isoweekday(self) -> int:
        """Return the ISO weekday of the date (1=Monday, 7=Sunday)."""
        return self.date.isoweekday()
    

class Time(StringPattern):
    """Time is a string in the format HH:MM:SS.

    Example: 12:00:00

    This class mimics the datetime.time class, and provides a time property
    """
    pattern = fr"^{TimePattern}$"

    def __new__(cls, value):
        string = super().__new__(cls, value)
        string.hour = int(value[:2])
        string.minute = int(value[3:5])
        string.second = int(value[6:8])
        string.time = datetime.strptime(value, "%H:%M:%S").time()

    def replace(self, **kwargs) -> "Time":
        """Return a new Time with the same values, but with specified
        parameters updated.
        """
        new_time = datetime.strptime(self, "%H:%M:%S").time().replace(**kwargs)
        return Time(new_time.strftime("%H:%M:%S"))
    
    def isoformat(self) -> str:
        """Return the time in ISO 8601 format (HH:MM:SS)."""
        return self.time.isoformat()
    

class Datetime(StringPattern):
    """Datetime is a string in ISO 8601 format.

    Example: 2023-10-01T12:00:00Z

    This class mimics the datetime.datetime class, and provides a datetime
    """
    pattern = fr"^{DatetimePattern}$"

    def __new__(cls, value):
        string = super().__new__(cls, value)
        string.datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        string.date = Date(string.datetime.strftime("%Y-%m-%d"))
        string.time = Time(string.datetime.strftime("%H:%M:%S"))
        return string
    
    def date(self) -> Date:
        """Return the date part of the datetime."""
        return self.date
    
    def time(self) -> Time:
        """Return the time part of the datetime."""
        return self.time
    
    @property
    def year(self) -> int:
        """Return the year of the datetime."""
        return self.datetime.year
    
    @property
    def month(self) -> int:
        """Return the month of the datetime."""
        return self.datetime.month
    
    @property
    def day(self) -> int:
        """Return the day of the datetime."""
        return self.datetime.day
    
    @property
    def hour(self) -> int:
        """Return the hour of the datetime."""
        return self.datetime.hour
    
    @property
    def minute(self) -> int:
        """Return the minute of the datetime."""
        return self.datetime.minute
    
    @property
    def second(self) -> int:
        """Return the second of the datetime."""
        return self.datetime.second
    
    def replace(self, **kwargs) -> "Datetime":
        """Return a new Datetime with the same values, but with specified
        parameters updated.
        """
        new_datetime = self.datetime.replace(**kwargs)
        return Datetime(new_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
    
    def weekday(self) -> int:
        """Return the weekday of the datetime (0=Monday, 6=Sunday)."""
        return self.datetime.weekday()
    
    def isoweekday(self) -> int:
        """Return the ISO weekday of the datetime (1=Monday, 7=Sunday)."""
        return self.datetime.isoweekday()

    def isocalendar(self) -> tuple[int, int]:
        """Return the ISO calendar of the datetime (year, week number)."""
        return self.datetime.isocalendar()
