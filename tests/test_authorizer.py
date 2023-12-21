from enum import Enum, auto

import pytest
from flask import Flask, abort

from authorization import Authorizer


class AuthorizationGroup(Enum):
    EMPLOYEE = auto()
    MANAGER = auto()
    ADMIN = auto()


class Permissions(Enum):
    VIEW = auto()
    EDIT = auto()
    DELETE_PROJECT = auto()


def get_authorization_group_permissions(
    authorization_group: AuthorizationGroup,
) -> list[Permissions]:
    """Business logic for mapping AuthorizationGroup to Permissions comes here."""
    return {
        AuthorizationGroup.EMPLOYEE: [Permissions.VIEW],
        AuthorizationGroup.MANAGER: [Permissions.VIEW, Permissions.EDIT],
        AuthorizationGroup.ADMIN: [Permissions.EDIT, Permissions.DELETE_PROJECT],
    }[authorization_group]


class User:
    def __init__(
        self, username: str, authorization_groups: set[AuthorizationGroup]
    ) -> None:
        self.username = username
        self.authorization_groups = authorization_groups

    def permissions(self) -> set[Permissions]:
        permissions = set()
        for group_membership in self.authorization_groups:
            permissions.update(get_authorization_group_permissions(group_membership))
        return permissions


def load_employee() -> User:
    """Load employee for testing purposes"""
    return User(
        "Joe Test Employee",
        {
            AuthorizationGroup.EMPLOYEE,
        },
    )


def load_manager() -> User:
    """Load manager for testing purposes"""
    return User(
        "Alice Test Manager",
        {
            AuthorizationGroup.MANAGER,
        },
    )


def load_admin() -> User:
    """Load admin for testing purposes"""
    return User(
        "John Test Admin",
        {
            AuthorizationGroup.ADMIN,
        },
    )


def forbidden() -> None:
    raise PermissionError("403 Forbidden")


def user_can_view(user: User) -> bool:
    return Permissions.VIEW in user.permissions()


def user_can_edit(user: User) -> bool:
    return Permissions.EDIT in user.permissions()


def user_can_delete_project(user: User) -> bool:
    return Permissions.DELETE_PROJECT in user.permissions()


class TestAuthorizerEmployee:
    def test_authorizer__view(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_view)
        def view_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert view_project() == "Success"

    def test_authorizer__edit_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_edit)
        def edit_project():
            return "Success"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            edit_project()

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"

    def test_authorizer__delete_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_delete_project)
        def delete_project():
            return "Success"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            delete_project()

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"


class TestAuthorizerManager:
    def test_authorizer__view(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_manager, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_view)
        def view_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert view_project() == "Success"

    def test_authorizer__edit_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_manager, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_edit)
        def edit_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert edit_project() == "Success"

    def test_authorizer__delete_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_manager, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_delete_project)
        def delete_project():
            return "Success"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            delete_project()

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"


class TestAuthorizerAdmin:
    def test_authorizer__view(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_admin, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_view)
        def view_project():
            return "Success"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            view_project()

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"

    def test_authorizer__edit_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_admin, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_edit)
        def edit_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert edit_project() == "Success"

    def test_authorizer__delete_project(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_admin, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(user_can_delete_project)
        def delete_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert delete_project() == "Success"


class TestFunctionWithArguments:
    def test_function_with_arguments__allowed(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function with an input parameter that requires view permission
        @authorizer.requires_permission(user_can_view)
        def greet_user(name: str):
            return f"Hello {name}!"

        # WHEN the function is called
        # THEN function can be run
        assert greet_user("John") == "Hello John!"

    def test_function_with_arguments__forbidden(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function with an input parameter that requires delete_project permission
        @authorizer.requires_permission(user_can_delete_project)
        def greet_user(name: str):
            return f"Hello {name}!"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            greet_user("John")

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"

    def test_function_with_keyword_arguments__allowed(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function with an input parameter that requires delete_project permission
        @authorizer.requires_permission(user_can_view)
        def example_function(*args, **kwargs):
            return f"Positional arguments: {args}, keyword arguments: {kwargs}!"

        # WHEN the function is called
        # THEN function can be run
        assert (
            example_function(1, 2, 3, name="John", age=32)
            == "Positional arguments: (1, 2, 3), keyword arguments: {'name': 'John', 'age': 32}!"
        )

    def test_function_with_keyword_arguments__forbidden(self):
        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function with an input parameter that requires delete_project permission
        @authorizer.requires_permission(user_can_delete_project)
        def example_function(*args, **kwargs):
            return f"Positional arguments: {args}, keyword arguments: {kwargs}!"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            example_function(1, 2, 3, name="John", age=32)

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"


class TestExoticConditions:
    def test_authorizer_with_exotic_conditions__allowed(self):
        def only_allow_users_whose_name_starts_with_letter_a(user: User) -> bool:
            return user.username[0] == "A"

        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_manager, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(
            only_allow_users_whose_name_starts_with_letter_a
        )
        def view_project():
            return "Success"

        # WHEN the function is called
        # THEN function can be run
        assert view_project() == "Success"

    def test_authorizer_with_exotic_conditions__forbidden(self):
        def only_allow_users_whose_name_starts_with_letter_a(user: User) -> bool:
            return user.username[0] == "A"

        # GIVEN an Authorizer instance
        authorizer = Authorizer(load_employee, forbidden)

        # AND a function that requires delete_project permission
        @authorizer.requires_permission(
            only_allow_users_whose_name_starts_with_letter_a
        )
        def view_project():
            return "Success"

        # WHEN the function is called
        # THEN the forbidden function is run
        with pytest.raises(PermissionError) as error:
            view_project()

        # AND the specified message is returned
        assert str(error.value) == "403 Forbidden"


class TestAuthorizerFlask:
    def test_home(self):
        # GIVEN a forbidden function
        def flask_forbidden():
            abort(403, "Forbidden: you do not have access to this resource")

        # AND a Flask instance
        app = Flask(__name__)
        # AND an Authorizer
        authorizer = Authorizer(load_employee, flask_forbidden)

        @app.route("/")
        @authorizer.requires_permission(user_can_view)
        def hello_world():
            return "<p>Hello World!</p>"

        # WHEN the home page is loaded
        with app.test_client() as client:
            response = client.get("/")
        # THEN a 200 status is returned
        assert response.status_code == 200
        # AND the correct data
        assert response.data == b"<p>Hello World!</p>"

    def test_delete_project(self):
        # GIVEN a forbidden function
        def flask_forbidden():
            abort(403, "Forbidden: you do not have access to this resource")

        # AND a Flask instance
        app = Flask(__name__)
        # AND an Authorizer
        authorizer = Authorizer(load_employee, flask_forbidden)

        @app.route("/delete_project/<int:project_id>/")
        @authorizer.requires_permission(user_can_delete_project)
        def delete_project(project_id: int):
            return f"<p>Deleted project {project_id}</p>"

        # WHEN the home page is loaded
        with app.test_client() as client:
            response = client.get("/delete_project/23415/")
        assert response.status_code == 403
        assert b"Forbidden: you do not have access to this resource" in response.data
