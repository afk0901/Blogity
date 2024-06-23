"""This module is designed exclusively for the automatic testing of user
management features within the API.

It encompasses a comprehensive suite of tests covering user creation, authentication,
data retrieval, update functionalities, and deletion restrictions to ensure the
application's user management system operates as expected.

Utilizing Django's TestCase framework, Django REST Framework's APIClient for API
interactions, and model_bakery for model instance generation, this module facilitates
automated testing scenarios under various conditions, including both authenticated and
unauthenticated user actions.

The aim is to guarantee security, integrity, and proper authorization across all user
management operations through a systematic and automated testing approach.
"""

import datetime
import re
from http import HTTPStatus
from typing import Match, TypedDict

from django.forms import model_to_dict
from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized_class
from rest_framework.response import Response
from rest_framework.test import APIClient

from Authentication.client import Client
from Users.models import CustomUser


class AuthenticationResponseClientType(TypedDict):
    """Defines the type for responses from authentication and the client used
    for authenticated requests."""

    authentication_response: Response
    client: APIClient


class PostDataResponse(TypedDict):
    """Defines the type for post data and its corresponding response."""

    post_data: dict[str, int | str]
    response: Response


class UserResponsePostDataCustomUserType(AuthenticationResponseClientType):
    """Extends AuthenticationResponseClientType to include user response, post
    data, and a CustomUser instance."""

    user_response: Response
    post_data: dict[str, str | int]
    custom_user_instance: CustomUser


class TestUser:
    """Provides static_files methods for creating and authenticating users,
    along with utility methods for testing."""

    @staticmethod
    def create_user_response() -> PostDataResponse:
        """Create a user using the APIClient and returns the post data and
        response.

        :return: A dictionary containing post_data and the response from creating a
            user.
        """
        client = APIClient()
        post_data = model_to_dict(baker.prepare(CustomUser))
        return {
            "post_data": post_data,
            "response": client.post("/api/users/", post_data, format="json"),
        }

    @staticmethod
    def authenticate_user_client(
        username: str | int, password: str | int
    ) -> AuthenticationResponseClientType:
        """Authenticate a user and returns the authentication response and a
        client configured with authentication token.

        :param username: The username of the user to authenticate.
        :param password: The password of the user to authenticate.
        :return: A dictionary containing the authentication response and an
            authenticated client.
        """
        client = APIClient()
        response = client.post(
            "/api/token/",
            {"username": username, "password": password},
            format="json",
        )
        authentication_token = response.data["access"]

        return {
            "authentication_response": response,
            "client": APIClient(
                headers={"Authorization": "Bearer " + authentication_token}
            ),
        }

    @staticmethod
    def create_test_user(
        authenticated: bool = True,
    ) -> UserResponsePostDataCustomUserType:
        """Create a test user and optionally authenticates it, returning
        relevant data and objects for testing.

        :param authenticated: Whether to authenticate the created user. Defaults to
            True.
        :return: A dictionary containing the user's response, post data, custom user
            instance, authentication response, and client.
        """
        create_user_response = TestUser.create_user_response()
        user_post_data = create_user_response["post_data"]

        authenticate_user_client = TestUser.authenticate_user_client(
            username=user_post_data["username"],
            password=user_post_data["password"],
        )

        authenticated_client = authenticate_user_client["client"]
        authenticate_response = authenticate_user_client["authentication_response"]

        client = Client.get_client(
            authenticated_client=authenticated_client,
            authenticate=authenticated,
        )

        return {
            "user_response": create_user_response["response"],
            "post_data": user_post_data,
            "custom_user_instance": CustomUser.objects.get(
                username=user_post_data["username"]
            ),
            "authentication_response": authenticate_response,
            "client": client,
        }

    @staticmethod
    def password_is_hashed(username: str) -> Match[str] | None:
        """Check if the password for the given username is hashed.

        :param username: The username of the user whose password to check.
        :return: A match object if the password is hashed; None otherwise.
        """
        user = CustomUser.objects.get(username=username)
        # Starts with the hash prefix, then iterations (some numbers)
        # and then the hash itself that can be anything
        hash_regex = r"^pbkdf2_sha256\$\d+.*"
        return re.match(hash_regex, user.password)


@parameterized_class(
    ("authenticate",),
    [
        (True,),
        (False,),
    ],
)
class CreatedUserSuccessfullyTestCases(TestCase):
    """Tests the creation of a user through a post-request and verifies
    successful creation and data accuracy."""

    # For type checkers and for clarity.
    authenticate: bool
    response: Response
    request_data: dict[str, str | int]

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data for the class by creating a test user with the
        specified authentication response."""
        create_test_user = TestUser.create_test_user(authenticated=cls.authenticate)
        cls.response = create_test_user["user_response"]
        cls.request_data = create_test_user["post_data"]

    def test_created_user_status(self) -> None:
        """Verifies that the user was created with the correct HTTP status
        code."""
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_created_user_successfully_response(self) -> None:
        """Checks if the response data matches the request data for username,
        first_name, and last_name."""
        self.assertEqual(self.response.data["username"], self.request_data["username"])
        self.assertEqual(
            self.response.data["first_name"], self.request_data["first_name"]
        )
        self.assertEqual(
            self.response.data["last_name"], self.request_data["last_name"]
        )

    def test_response_should_not_contain_password_field(self) -> None:
        """Ensures that the response does not contain a password field."""
        self.assertNotIn("password", self.response.data)

    def test_password_is_hashed(self) -> None:
        """Verifies that the user's password is properly hashed in the
        database."""
        self.assertTrue(
            TestUser.password_is_hashed(username=self.response.data["username"])
        )


class AuthenticateUserTestCases(TestCase):
    """Tests the authentication process for a user, ensuring tokens are
    received upon successful authentication."""

    def setUp(self) -> None:
        """Set up the test case by creating and authenticating a test user."""
        self.auth_response = TestUser.create_test_user()["authentication_response"]

    def test_user_created_and_authenticated(self) -> None:
        """Verifies that the authentication response contains access and
        refresh tokens."""
        self.assertContains(self.auth_response, "access", status_code=HTTPStatus.OK)
        self.assertContains(self.auth_response, "refresh", status_code=HTTPStatus.OK)


# @parameterized_class(
#     ("authenticate",),
#     [
#         (True,),
#         (False,),
#     ],
# )
class GetIndividualUser(TestCase):
    """Tests the retrieval of individual user data, ensuring correct status
    code and data integrity."""

    authenticate: bool
    resp: Response

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data by creating a test user and making a GET request
        for that user's data."""
        create_test_user = TestUser.create_test_user()
        authenticated_client = create_test_user["client"]
        client = Client.get_client(authenticated_client, True)
        user_id = CustomUser.objects.latest("id").id
        cls.resp = client.get(f"/api/users/{user_id}/")

    def test_get_individual_user_status_code(self) -> None:
        """Checks if the HTTP status code for retrieving an individual user is
        OK."""
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_get_individual_user(self) -> None:
        """Verifies that the response data includes id, username, first_name,
        last_name, and excludes the password."""
        self.assertIn("id", self.resp.data)
        self.assertIn("username", self.resp.data)
        self.assertIn("first_name", self.resp.data)
        self.assertIn("last_name", self.resp.data)
        self.assertNotIn("password", self.resp.data)


class UpdateIndividualUser(TestCase):
    """Tests the update functionality for individual user's data, ensuring data
    integrity and authorization checks."""

    user_id: int
    new_user: dict[str, int | str]
    updated_user_response: Response
    old_user: Response

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data by creating a test user, retrieving the user's
        data, and then attempting to update it."""
        test_user = TestUser.create_test_user()
        authenticated_client = test_user["client"]
        cls.user_id = CustomUser.objects.latest("id").id
        cls.old_user = authenticated_client.get(f"/api/users/{cls.user_id}/")
        cls.new_user = model_to_dict(
            baker.prepare(CustomUser, id=1, last_login=datetime.datetime.now())
        )

        cls.updated_user_response = authenticated_client.put(
            f"/api/users/{cls.user_id}/", data=cls.new_user
        )

    def test_update_individual_user_status_code(self) -> None:
        """Verifies the HTTP status code is OK for updating a user's data."""
        self.assertEqual(self.updated_user_response.status_code, HTTPStatus.OK)

    def test_update_individual_user(self) -> None:
        """Checks if the updated user's data matches the new data provided and
        differs from the old data."""
        self.assertNotEqual(
            self.updated_user_response.data["username"],
            self.old_user.data["username"],
        )
        self.assertNotEqual(
            self.updated_user_response.data["first_name"],
            self.old_user.data["first_name"],
        )
        self.assertNotEqual(
            self.updated_user_response.data["last_name"],
            self.old_user.data["last_name"],
        )

        self.assertEqual(
            self.updated_user_response.data["username"],
            self.new_user["username"],
        )
        self.assertEqual(
            self.updated_user_response.data["first_name"],
            self.new_user["first_name"],
        )
        self.assertEqual(
            self.updated_user_response.data["last_name"],
            self.new_user["last_name"],
        )

    def test_password_is_hashed(self) -> None:
        """Confirms that the user's password remains hashed after updating."""
        self.assertTrue(
            TestUser.password_is_hashed(
                username=self.updated_user_response.data["username"]
            )
        )

    def test_only_authorized_owner_can_update(self) -> None:
        """Ensures that only the authorized user (owner) can update their data,
        testing with a forbidden status."""
        updated_user_response = TestUser.create_test_user()["client"].put(
            f"/api/users/{self.user_id}/",
            data=self.new_user,
            content_type="application/json",
        )

        self.assertEqual(updated_user_response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthorized_user_cant_update_status_code(self) -> None:
        """Ensures that an unauthorized user cannot update user data, expecting
        an unauthorized status code."""
        resp = APIClient().put(
            f"/api/users/{self.user_id}/",
            data=self.new_user,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


class UserCantDelete(TestCase):
    """Ensures users cannot delete their own or other users' data, enforcing
    method restrictions and authorization."""

    current_user_id: int
    resp: Response

    @classmethod
    def setUpTestData(cls) -> None:
        """Prepare test data by creating a user and attempting to delete it."""
        create_test_user = TestUser.create_test_user()
        cls.current_user_id = create_test_user["user_response"].data["id"]
        cls.resp = create_test_user["client"].delete(
            f"/api/users/{cls.current_user_id}/"
        )

    def test_user_cant_delete_it_self_status_code(self) -> None:
        """Verifies that a user cannot delete their own account, expecting a
        method not allowed status code."""
        self.assertEqual(self.resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_authenticated_user_cant_delete_another_user_status_code(
        self,
    ) -> None:
        """Checks that an authenticated user cannot delete another user's data,
        expecting method not allowed status."""
        create_test_user = TestUser.create_test_user()
        current_user_id = create_test_user["user_response"].data["id"]
        resp = create_test_user["client"].delete(f"/api/users/{current_user_id - 1}/")
        self.assertEqual(resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_unauthorized_user_cant_delete_a_user_status_code(self) -> None:
        """Ensures that an unauthorized user cannot delete a user data,
        expecting a method not allowed status code."""
        resp = APIClient().delete(
            f"/api/users/{self.current_user_id}/",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
