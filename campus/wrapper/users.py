"""campus/operations/users

Represents operations on the users resource in Campus.
"""

from campus.schema.datatypes import UserID, Validatable
from campus.schema.modeltypes import User as UserModel
from campus.wrapper.base import SingleResource, ResourceCollection

from . import http


class User(SingleResource):
    """Represents operations on a single user resource in Campus."""

    def activate(self) -> None:
        """.users[{user_id}].activate()"""
        api_path = self.build_path('activate')
        http.post(api_path)
    
    def delete(self) -> None:
        """.users[{user_id}].delete()"""
        api_path = self.build_path()
        http.delete(api_path)

    def get(self) -> UserModel:
        """.users[{user_id}].get()"""
        api_path = self.build_path()
        resp_json = http.get(api_path)
        return UserModel(**resp_json)

    def update(self, **kwargs: Validatable) -> None:
        """.users[{user_id}].update(...)"""
        User.validate_request(kwargs)
        api_path = self.build_path()
        http.put(api_path, data=kwargs)

    
class Users(ResourceCollection):
    """Represents operations on users in Campus."""

    def __getitem__(self, user_id: str) -> User:
        """.users[{user_id}]"""
        UserID.validate(user_id)
        return User(self, UserID(user_id))

    def new(self, **kwargs: Validatable) -> User:
        """.users.new(...)"""
        user = UserModel(**kwargs)
        api_path = self.build_path()
        http.post(api_path, data=user.as_json())
        return User(self, user.id)

