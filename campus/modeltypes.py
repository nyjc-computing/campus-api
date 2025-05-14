from collections.abc import Mapping

from .datatypes import (
    Schema,
    BasicSchema,
    String,
    Number,
    Integer,
    Boolean,
    Array,
    Object,
    BasicType,
    UID,
    ShortUID,
    LongUID,
    CampusID,
    UserID,
    ClientID,
    CampusWord,
    CampusName,
    CircleID,
    OTP,
)


class CampusUser(Mapping, Object):
    """Campus user model.

    This model is used to represent a user in the campus system.
    """

    def __init__(self, **fields):
        super().__init__(**fields)
        self.data = fields

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"
    
    @property
    def id(self) -> UserID:
        return UserID(self.data["id"])
    


class CampusModel(Mapping, Object):
    """Base class for all campus models (besides User).

    All campus models must inherit from this class.
    """

    def __init__(self, **fields):
        self.data = fields

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"
    
    @property
    def id(self) -> CampusID

    def to_dict(self) -> dict:
        """Convert the model to a json dictionary."""
