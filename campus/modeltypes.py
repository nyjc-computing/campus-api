from typing import Any

from openapi.schema.datatypes import format_keyvalues

from .datatypes import (
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
    # Models must declare all properties as class variables.
    # Properties must use the Validatable type.

    def __init_subclass__(cls, **kwargs):
        """__init_subclass__ is called when a subclass is created, not when an
        instance is created.

        This init hook is used to validate properties and provide a validators
        class variable.
        """
        cls.validators = {}
        for field, typecls in cls.validators.items():
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


class User(CampusModel):
    """Campus user model.

    This model is used to represent a user in the campus system.
    """
    __response_only__ = ("id", "activated_at")
    id: UserID
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
