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
    # Models must declare all properties as class variables.
    # Properties must use the Validatable type.

    def __init_subclass__(cls, **kwargs):
        """__init_subclass__ is called when a subclass is created, not when an
        instance is created.

        This init hook is used to validate properties and provide a validators
        class variable.
        """
        cls.validators = dict(cls.__annotations__.items())
        for field, typecls in cls.validators.items():
            if not isinstance(typecls, Validatable):
                raise TypeError(f"Field {field} must be of type Validatable")

    def __init__(self, **kwargs):
        """__init__ is called when an instance is created.

        The init method checks for missing and invalid fields, and validates
        the given keyword arguments.
        """
        invalid_fields = set(kwargs) - set(self.validators)
        missing_fields = set(self.validators) - set(kwargs)
        if invalid_fields:
            raise KeyError(f"Invalid fields: {invalid_fields}")
        if missing_fields:
            raise KeyError(f"Missing fields: {missing_fields}")
        for field, Typecls in self.validators:
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
    id: UserID
    email: EmailAddress    


class Client(CampusModel):
    """Campus client model.

    This model is used to represent a client in the campus system.
    """
    id: CampusID
    name: CampusLabel
    description: String
    created_at: Datetime
    secret_hash: Base64String
