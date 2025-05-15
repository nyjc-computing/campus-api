"""campus/operations/users

Represents operations on the users resource in Campus.
"""

from campus.schema.datatypes import UserID, Validatable
from campus.schema.modeltypes import User
from campus.wrapper.base import SingleResource, ResourceCollection


class User(SingleResource):
    """Represents operations on a single user resource in Campus.
    """

    def activate(self) -> None:
        """.users[{user_id}].activate()"""
    
    def delete(self) -> None:
        """.users[{user_id}].delete()"""
        # TODO: API call to delete user

    def get(self) -> User:
        """.users[{user_id}].get()"""
        # TODO: API call to get user

    def update(self, **kwargs: Validatable) -> None:
        """.users[{user_id}].update(...)"""
        User.validate_request(kwargs)
        # TODO: API call to update user

    
class Users(ResourceCollection):
    """Represents operations on users in Campus."""

    def __getitem__(self, user_id: str) -> User:
        """Get a user by ID."""
        UserID.validate(user_id)
        return User(self, UserID(user_id))

    def new(self, **kwargs: Validatable) -> User:
        """.clients.new(...)"""
        user = User(**kwargs)
        # TODO: API call to post user
        return User

