from rest_framework.test import APIClient
from django.test import TestCase
from http import HTTPStatus

from Users.models import CustomUser
from model_bakery import baker
from django.forms import model_to_dict
from Authentication.client import Client
from parameterized import parameterized_class

import datetime


class TestUser:
    @staticmethod
    def create_user_response():
        """
        :return: Post_data and response
        """
        client = APIClient()
        post_data = model_to_dict(baker.prepare(CustomUser))
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
        create_user_response = TestUser.create_user_response()
        user_post_data = create_user_response["post_data"]

        # Authenticate
        authenticate_user_client = TestUser.authenticate_user_client(username=user_post_data["username"],
                                                                     password=user_post_data["password"])

        client = authenticate_user_client["client"]
        authenticate_response = authenticate_user_client["authentication_response"]

        return {"user_data": create_user_response["response"].data,
                "custom_user_instance": CustomUser.objects.get(username=user_post_data["username"]),
                "authenticate_response": authenticate_response,
                "authenticated_client": client
                }


class CreatedUserSuccessfullyTestCases(TestCase):
    """
    Makes a post-request and checks if the user has been created successfully.
    """

    def setUp(self):
        create_user_response = TestUser.create_user_response()
        self.response = create_user_response["response"]
        self.request_data = create_user_response["post_data"]

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


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class GetIndividualUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_authenticated_test_user = TestUser.create_authenticated_test_user()
        authenticated_client = create_authenticated_test_user["authenticated_client"]
        client = Client.get_client(authenticated_client, cls.authenticate)
        user_id = CustomUser.objects.last().id
        cls.resp = client.get(f"/api/users/{user_id}/")

    def test_get_individual_user_status_code(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.OK)

    def test_get_individual_user(self):
        self.assertIn("id", self.resp.data)
        self.assertIn("username", self.resp.data)
        self.assertIn("first_name", self.resp.data)
        self.assertIn("last_name", self.resp.data)


class UpdateIndividualUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_authenticated_test_user = TestUser.create_authenticated_test_user()
        authenticated_client = create_authenticated_test_user["authenticated_client"]
        user_id = CustomUser.objects.last().id
        cls.old_user = authenticated_client.get(f"/api/users/{user_id}/")
        cls.new_user = model_to_dict(baker.prepare(CustomUser, id=1, last_login=datetime.datetime.now()))

        cls.updated_user_response = authenticated_client.put(f"/api/users/{user_id}/",
                                            data=cls.new_user)

    def test_update_individual_user_status_code(self):
        self.assertEqual(self.updated_user_response.status_code, HTTPStatus.OK)

    def test_update_individual_user(self):
        self.assertNotEqual(self.updated_user_response.data["username"], self.old_user.data["username"])
        self.assertNotEqual(self.updated_user_response.data["first_name"], self.old_user.data["first_name"])
        self.assertNotEqual(self.updated_user_response.data["last_name"], self.old_user.data["last_name"])

        self.assertEqual(self.updated_user_response.data["username"], self.new_user["username"])
        self.assertEqual(self.updated_user_response.data["first_name"], self.new_user["first_name"])
        self.assertEqual(self.updated_user_response.data["last_name"], self.new_user["last_name"])


class UserCantDeleteItSelf(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_authenticated_test_user = TestUser.create_authenticated_test_user()
        authenticated_client = create_authenticated_test_user["authenticated_client"]
        current_user_id = create_authenticated_test_user["user_data"]["id"]
        cls.resp = authenticated_client.delete(f"/api/users/{current_user_id}/")

    def test_user_cant_delete_it_self_status_code(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
