from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from Permissions.author_permissions import IsAuthorAnyRead
from unittest.mock import Mock


class AuthorPermissionTest(SimpleTestCase):

    """
    Unit tests the custom permission classes for the
    author of a blog post or blog comment.
    """

    def setUp(self):
        self.user = Mock()
        self.other_user = Mock()

        self.user.username = 'user'
        self.user.id = 1
        self.other_user.username = 'other_user'
        self.other_user.id = 2

        self.permission = IsAuthorAnyRead()

        # Faking the object. Object should have the author as some user
        self.author_object = Mock()
        self.author_object.author_id = self.user.id

        # REST API request factory
        self.factory = APIRequestFactory()

        self.list_view_url = '/some-url/'

        self.detail_view_url = '/some-url/1/'

    def post_request(self, user):
        """
         Simulates a post-request without performing one.
        :param user: The user performing the request
        :return: Post request with an extra data attribute
        """
        data = {
            "author_id": self.user.id,
            "title": "",
            "content": ""
        }

        request = self.factory.post(self.list_view_url)
        request.data = data
        request.user = user
        return request

    def test_has_object_permission_owner(self):
        # User should have full permission over the object if the user is the author
        request = self.factory.get(self.list_view_url)
        request.user = self.user
        # Even tho this is a get request, the data attribute will be included
        # leading to a 500 error if it does not contain the desired key.
        request.data = {}
        self.assertTrue(self.permission.has_object_permission(request, "", self.author_object))

    def test_has_permission_owner(self):
        # User should be the author of the object and to be able to have full list
        # permissions.
        request = self.post_request(self.user)
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_not_owner_deny_add_to_list(self):

        request = self.post_request(self.other_user)
        self.assertFalse(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_user(self):
        # Because everybody should be able to have read access
        request = self.factory.get(self.list_view_url)
        request.user = self.user
        # We put in some author data because it should not matter in this case
        # if the consumer sends data with the GET request.
        request.data = {"author": 18,
                        "post": 4,
                        "content": "Esta bem!"
                        }
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_other_user(self):
        # Because everybody should be able to have read access, not just the user that
        # is the author
        request = self.factory.get(self.list_view_url)
        request.user = self.other_user
        request.data = {}
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_user_request_data_but_no_author(self):
        # Because everybody should be able to have read access
        request = self.factory.get(self.list_view_url)
        request.user = self.user
        # We put in some author data because it should not matter in this case
        # if the consumer sends data with the GET request.
        request.data = {}
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_true_user_details(self):
        request = self.factory.get(self.detail_view_url)
        request.user = self.user
        request.data = {}
        self.assertTrue(self.permission.has_object_permission(request, "", self.author_object))

    def test_has_permission_get_true_true_other_user_details(self):
        request = self.factory.get(self.detail_view_url)
        request.user = self.other_user
        request.data = {}
        self.assertTrue(self.permission.has_object_permission(request, "", self.author_object))
