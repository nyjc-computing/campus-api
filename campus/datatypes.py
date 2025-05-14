from openapi.datatypes import (
    Schema,
    BasicSchema,
    String,
    Number,
    Integer,
    Boolean,
    Array,
    Object
)

class UID(String):
    """Campus IDs are based on shortened, base64-encoded UUIDs.

    They only use lowercase letters and numbers for ease of use.

    Campus IDs have 2 lengths:
    - short: 8 characters
    - long: 16 characters
    """
    type = "string"
    format = "campus_id"

class ShortUID(UID):
    """Shortened UID with 8 characters."""
    pattern = r"^[a-z0-9]{8}$"
    min_length = 8
    max_length = 8

class LongUID(UID):
    """Long UID with 16 characters."""
    pattern = r"^[a-z0-9]{16}$"
    min_length = 16
    max_length = 16

class CampusID(UID):
    """Campus IDs are UIDs prefixed with a namespace.

    The namespace is 'uid-' followed by a string of hyphenated lowercase words,
      with up to 3 parts.

    Example: uid-client-12345678
    """
    pattern = r"uid-([a-z]{2,16}(-[a-z]{2,16}){0,2})-^[a-z0-9]{8}|[a-z0-9]{16}$"
    min_length = 8
    max_length = 16

class UserID(String):
    """User ID is the username component of the email address, assumed to be
      unique within a campus.

    Example: user.name_2024
    """
    pattern = r"^[a-zA-Z0-9._-]{1,64}$"
    min_length = 1
    max_length = 64
    format = "user_id"

class ClientID(ShortUID):
    """UID to identify a client.
    
    Example: uid-client-12345678
    """
    pattern = r"^uid-client-[a-z0-9]{8}$"
    min_length = 8
    max_length = 8
    format = "client_id"

class CampusWord(String):
    """Campus word is a string of lowercase letters, with a length between 2
      and 15 characters.

    Example: nyjc
    """
    pattern = r"^[a-z]{2,15}$"
    min_length = 2
    max_length = 15
    format = "campus_word"

class CampusName(String):
    """Campus name is a string of lowercase letters, with a length between 2
      and 15 characters, and can have up to 2 hyphenated parts.

    Example: nyjc-north
    """
    pattern = r"^[a-z]{2,15}(-[a-z]{2,15}){0,2}$"
    min_length = 2
    max_length = 15
    format = "campus_name"

class CircleID(ShortUID):
    """UID to identify a circle.

    Example: uid-circle-12345678
    """
    pattern = r"^uid-circle-[a-z0-9]{8}$"
    min_length = 8
    max_length = 8
    format = "circle_id"

class OTP(String):
    """One-time password (OTP) is a 6-digit number.

    Example: 123456
    """
    pattern = r"^[0-9]{6}$"
    min_length = 6
    max_length = 6
    format = "otp"
