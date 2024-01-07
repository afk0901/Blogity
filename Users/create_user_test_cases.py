from rest_framework.test import APIClient
from django.test import TestCase


class CreatedUserSuccessfullyTestCases(TestCase):

    """
    Makes a post-request and checks if the user has been created successfully.
    """
    def setUp(self):
        data = {
            "username": 'tester',
            "first_name": "Jackie",
            "last_name": "Test",
            "password": "test"
        }
        self.response_data = data
        self.response = APIClient().post('/api/users/', data, format='json')

    def test_created_user_status(self):
        self.assertEqual(self.response.status_code, 201)

    def test_created_user_response(self):
        self.assertEqual(self.response.data['username'], self.response_data["username"])
        self.assertEqual(self.response.data['first_name'], self.response_data["first_name"])
        self.assertEqual(self.response.data['last_name'], self.response_data["last_name"])

    def test_response_should_not_contain_password_field(self):
        # TODO: The functionality itself is not implemented yet.
        ...

    def test_created_user_error(self):
        # TODO: test the response on error.
        ...
