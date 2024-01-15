from rest_framework.test import APIClient
from django.test import TestCase


class TestUser:

    @staticmethod
    def test_user_post_data(user_id: int, username: str) -> dict[str, str]:
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
    def create_test_user_post_data_and_response():
        """
        :return: Dict of post_data and response
        """

        client = APIClient()
        post_data = TestUser.test_user_post_data(user_id=1, username="tester")
        return {"post_data": post_data, "response": client.post('/api/users/', post_data, format='json')}

    @staticmethod
    def authenticate(username: str, password: str):
        # Authenticate
        client = APIClient()
        client.post('api/token/', {'username': username, 'password': password}, format='json')

    @staticmethod
    def create_test_user_and_authenticate_response():
        """
        :return: The authentication response
        """
        # Create the user
        create_test_user_post_data_and_response = TestUser.create_test_user_post_data_and_response()
        user_post_data = create_test_user_post_data_and_response["post_data"]

        # Authenticate
        request_data = {"username": user_post_data["username"], "password": user_post_data["password"]}
        client = APIClient()
        auth_response = client.post('/api/token/', request_data, format='json')
        return {"user":  create_test_user_post_data_and_response["response"].data, "response": auth_response}


class CreatedUserSuccessfullyTestCases(TestCase):
    """
    Makes a post-request and checks if the user has been created successfully.
    """

    def setUp(self):
        create_test_user_post_data_and_response = TestUser.create_test_user_post_data_and_response()
        self.response = create_test_user_post_data_and_response["response"]
        self.request_data = create_test_user_post_data_and_response["post_data"]

    def test_created_user_status(self):
        self.assertEqual(self.response.status_code, 201)

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
        self.auth_response = TestUser.create_test_user_and_authenticate_response()["response"]

    def test_user_created_and_authenticated(self):
        self.assertContains(self.auth_response, 'access', status_code=200)
        self.assertContains(self.auth_response, 'refresh', status_code=200)
