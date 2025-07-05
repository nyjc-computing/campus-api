"""campus/schema/modeltypes

Campus API model types.
"""
from typing import Any, Mapping

from openapi.schema.datatypes import format_keyvalues

from campus.schema.datatypes import (
    Base64String,
    CampusID,
    CampusLabel,
    Date,
    Datetime,
    String,
    Time,
    UserID,
    EmailAddress,
    Validatable,
)


class CampusModel(dict[str, Validatable]):
    """Base class for all models.

    This class is used to represent a model in the campus system.
    Models subclass Python dict for easier compatibility with JSON.
    """
    # Hidden properties are not specified in requests, and not returned in responses
    __hidden__: tuple[str] = ()
    # Request-only properties are specified in requests, but not returned in responses
    __request_only__: tuple[str] = ()
    # Response-only properties are not specified in requests, but returned in responses
    __response_only__: tuple[str] = ()
    # Required properties are required in requests
    __required__: tuple[str] = ()
    # Models must declare all properties as class variables.
    # Properties must use the Validatable type.
    validators: dict[str, type[Validatable]]

    def __init_subclass__(cls, **kwargs):
        """__init_subclass__ is called when a subclass is created, not when an
        instance is created.

        This init hook is used to validate properties and provide a validators
        class variable.
        """
        cls.validators = {}
        for field, typecls in cls.__annotations__.items():
            if field == "validators" or field.startswith("__"):
                continue
            if not isinstance(typecls, Validatable):
                raise TypeError(f"Field {field} must be of type Validatable")
            if field in cls.__hidden__ and field in cls.__request_only__:
                raise TypeError(
                    f"Field {field} cannot be both hidden and request-only"
                )
            if field in cls.__hidden__ and field in cls.__response_only__:
                raise TypeError(
                    f"Field {field} cannot be both hidden and response-only"
                )
            if field in cls.__required__ and field in cls.__response_only__:
                raise TypeError(
                    f"Field {field} cannot be both required and response-only"
                )
            if field in cls.__required__ and field in cls.__hidden__:
                raise TypeError(
                    f"Field {field} cannot be both required and hidden"
                )
            cls.validators[field] = typecls

    def __init__(self, **kwargs):
        """__init__ is called when an instance is created.

        The init method checks for missing and invalid fields, and validates
        the given keyword arguments.
        """
        invalid_fields = set(kwargs) - set(self.validators)
        missing_fields = (
            set(self.validators)
            - set(kwargs)
            - set(self.__hidden__)
            - set(self.__response_only__)
        )
        if invalid_fields:
            raise KeyError(f"Invalid fields: {invalid_fields}")
        if missing_fields:
            raise KeyError(f"Missing fields: {missing_fields}")
        for field, Typecls in self.validators:
            if field in self.__hidden__:
                raise KeyError(
                    f"Field {field} is hidden and should not be passed in init"
                )
            if field in self.__response_only__:
                raise KeyError(
                    f"Field {field} is response-only and should not be passed in init"
                )
            assert isinstance(Typecls, Validatable)  # appease linter
            Typecls.validate(kwargs[field])
        # Cast all values to their respective Validatable types
        super().__init__(**{
            field: Typecls(kwargs[field])
            for field, Typecls in self.validators.items()
        })

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({format_keyvalues(self)})"
    
    def __getattr__(self, field: str) -> Validatable:
        """Get an attribute from the model.

        This method is used to get an attribute from the model.
        """
        if field in self:
            return self[field]
        raise AttributeError(f"{type(self).__name__}.{field}: no such field")
    
    def as_json(self) -> dict[str, Any]:
        """Return the model as a JSON-serialisable response."""
        return {
            field: value.as_json()
            for field, value in self.items()
            if not (field in self.__hidden__ or field in self.__request_only__)
        }
    
    @classmethod
    def validate_request(cls, request: Mapping[str, Any]) -> None:
        """Validate a request to the model.

        This method is used to validate a request to the model.
        """
        required_fields = list(cls.__required__)
        for field, value in request.items():
            if field not in cls.validators:
                raise KeyError(f"Invalid field: {field}")
            if field in cls.__hidden__:
                raise KeyError(f"Field {field} is hidden")
            if field in cls.__response_only__:
                raise KeyError(f"Field {field} is response-only")
            required_fields.remove(field)
            cls.validators[field].validate(value)
        if required_fields:
            raise KeyError(f"Required fields are missing: {required_fields}")


class User(CampusModel):
    """Campus user model.

    This model is used to represent a user in the campus system.
    """
    __response_only__ = ("id", "activated_at")
    id: UserID
    name: str
    email: EmailAddress
    activated_at: Datetime


class Client(CampusModel):
    """Campus client model.

    This model is used to represent a client in the campus system.
    """
    __hidden__ = ("secret_hash",)
    __response_only__ = ("id", "created_at")
    id: CampusID
    name: CampusLabel
    description: String
    created_at: Datetime
    secret_hash: Base64String


class Circle(CampusModel):
    """Campus circle model.

    This model is used to represent a circle in the campus system.
    """
    __response_only__ = ("id", "created_at", "members", "sources")
    __required__ = ("id", "name", "tag", "created_at")
    id: CampusID
    name: CampusLabel
    description: String
    tag: String
    members: dict[CampusID, int]
    created_at: Datetime
    sources: dict  # SourceID, SourceHeader


class CircleNew(CampusModel):
    """Request schema for creating a new circle."""
    __required__ = ("name", "tag")
    name: CampusLabel
    description: String
    tag: String
    parents: dict[String, int]  # CirclePath to AccessValue


class CircleUpdate(CampusModel):
    """Request schema for updating a circle."""
    __required__ = ()
    name: CampusLabel
    description: String


class CircleMemberAdd(CampusModel):
    """Request schema for adding a member to a circle."""
    __required__ = ("member_id", "access_value")
    member_id: CampusID
    access_value: int


class CircleMemberRemove(CampusModel):
    """Request schema for removing a member from a circle."""
    __required__ = ("member_id",)
    member_id: CampusID


class CircleMemberSet(CampusModel):
    """Request schema for setting a member's access in a circle."""
    __required__ = ("member_id", "access_value")
    member_id: CampusID
    access_value: int
