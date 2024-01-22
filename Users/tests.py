from rest_framework.test import APIClient
from django.test import TestCase
from http import HTTPStatus

from Users.models import CustomUser


class TestUser:

    @staticmethod
    def user_post_data(user_id: int, username: str) -> dict[str, str]:
        """
        :return: Dictionary of strings representing the user POST request data.
        """

        return {
            "id": user_id,
            "username": username,
            "first_name": "Jackie",
            "last_name": "Test",
            "password": "12345"
        }

    @staticmethod
    def create_user_post_data_and_response():
        """
        :return: Dict of post_data and response
        """

        client = APIClient()
        post_data = TestUser.user_post_data(user_id=1, username="tester")
        return {"post_data": post_data, "response": client.post('/api/users/', post_data, format='json')}

    @staticmethod
    def authenticate_user_client(username: str, password: str):
        client = APIClient()
        response = client.post('/api/token/', {'username': username, 'password': password}, format='json')
        authentication_token = response.data["access"]
        return {"authentication_response": response,
                "client": APIClient(headers={"Authorization": "Bearer " + authentication_token}
                                    )}

    @staticmethod
    def create_authenticated_test_user():

        # Create the user
        create_user_post_data_and_response = TestUser.create_user_post_data_and_response()
        user_post_data = create_user_post_data_and_response["post_data"]

        # Authenticate
        authenticate_user_client = TestUser.authenticate_user_client(username=user_post_data["username"],
                                                                     password=user_post_data["password"])

        client = authenticate_user_client["client"]
        authenticate_response = authenticate_user_client["authentication_response"]

        return {"user_data":  create_user_post_data_and_response["response"].data,
                "custom_user_instance": CustomUser.objects.get(username=user_post_data["username"]),
                "authenticate_response": authenticate_response,
                "authenticated_client": client
                }


class CreatedUserSuccessfullyTestCases(TestCase):
    """
    Makes a post-request and checks if the user has been created successfully.
    """

    def setUp(self):
        create_user_post_data_and_response = TestUser.create_user_post_data_and_response()
        self.response = create_user_post_data_and_response["response"]
        self.request_data = create_user_post_data_and_response["post_data"]

    def test_created_user_status(self):
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_created_user_successfully_response(self):
        self.assertEqual(self.response.data['username'], self.request_data["username"])
        self.assertEqual(self.response.data['first_name'], self.request_data["first_name"])
        self.assertEqual(self.response.data['last_name'], self.request_data["last_name"])

    def test_response_should_not_contain_password_field(self):
        # TODO: The functionality itself is not implemented yet.
        ...

    def test_created_user_error(self):
        # TODO: test the response on error.
        ...


class AuthenticatedUserTestCases(TestCase):

    def setUp(self):
        self.auth_response = TestUser.create_authenticated_test_user()["authenticate_response"]

    def test_user_created_and_authenticated(self):
        self.assertContains(self.auth_response, 'access', status_code=HTTPStatus.OK)
        self.assertContains(self.auth_response, 'refresh', status_code=HTTPStatus.OK)
