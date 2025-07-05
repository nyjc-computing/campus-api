"""campus/api/circles

Represents operations on the circles resource in Campus.
"""

from campus.schema.datatypes import CircleID, Validatable
from campus.schema.modeltypes import Circle as CircleModel
from campus.api.base import SingleResource, ResourceCollection

from . import http


class CircleMembers:
    """Represents operations on circle members."""

    def __init__(self, circle: "Circle"):
        self.circle = circle

    def list(self) -> dict:
        """Get member IDs of a circle and their access values."""
        api_path = self.circle.build_path('members')
        return http.get(api_path)

    def add(self, **kwargs: Validatable) -> http.JsonSerializable:
        """Add a member to a circle."""
        api_path = self.circle.build_path('members/add')
        return http.post(api_path, data=kwargs)

    def remove(self, **kwargs: Validatable) -> http.JsonSerializable:
        """Remove a member from a circle."""
        api_path = self.circle.build_path('members/remove')
        return http.delete(api_path, data=kwargs)

    def set(self, member_circle_id: str, **kwargs: Validatable) -> http.JsonSerializable:
        """Update a member's access in a circle."""
        api_path = self.circle.build_path('members', member_circle_id)
        return http.patch(api_path, data=kwargs)


class Circle(SingleResource):
    """Represents operations on a single circle resource in Campus."""

    @property
    def members(self) -> CircleMembers:
        return CircleMembers(self)

    def delete(self) -> http.JsonSerializable:
        """.circles[{circle_id}].delete()"""
        api_path = self.build_path()
        return http.delete(api_path)

    def get(self) -> CircleModel | None:
        """.circles[{circle_id}].get()"""
        api_path = self.build_path()
        resp_json = http.get(api_path)
        if 'error_code' in resp_json:
            self.root.handle_error(resp_json, api_path, 'GET')
        else:
            return CircleModel(**resp_json)

    def update(self, **kwargs: Validatable) -> http.JsonSerializable:
        """.circles[{circle_id}].update(...)"""
        # Circle.validate_request(kwargs)  # Uncomment if validation is available
        api_path = self.build_path()
        return http.patch(api_path, data=kwargs)

    def move(self, **kwargs: Validatable) -> http.JsonSerializable:
        """.circles[{circle_id}].move(...)"""
        api_path = self.build_path('move')
        # Not implemented on server, returns 501
        return http.post(api_path, data=kwargs)

    def users(self) -> http.JsonSerializable:
        """.circles[{circle_id}].users()"""
        api_path = self.build_path('users')
        # Not implemented on server, returns 501
        return http.get(api_path)


class Circles(ResourceCollection):
    """Represents operations on circles in Campus."""

    def __getitem__(self, circle_id: str) -> Circle:
        """.circles[{circle_id}]"""
        CircleID.validate(circle_id)
        return Circle(self, CircleID(circle_id))

    def new(self, **kwargs: Validatable) -> CircleModel:
        """.circles.new(...)"""
        circle = CircleModel(**kwargs)
        api_path = self.build_path()
        resp = http.post(api_path, data=circle.as_json())
        # The server returns the created resource as JSON
        return CircleModel(**resp)

