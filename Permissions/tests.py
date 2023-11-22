from django.test import TestCase
from rest_framework.test import APIRequestFactory
from Permissions.author_permissions import IsAuthor
from Users.models import CustomUser
from unittest.mock import Mock


class CustomPermissionTest(TestCase):

    def setUp(self):
        # Creating two distinct users
        self.user = CustomUser.objects.create_user(username='user', password='pass')
        self.other_user = CustomUser.objects.create_user(username='other_user', password='pass')
        self.permission = IsAuthor()

        # Faking the object. Object should have the author as some user
        self.author_object = Mock()
        self.author_object.author = self.user

        # REST API request factory
        self.factory = APIRequestFactory()

    def post_request(self, user):
        """
         Simulates a post-request without performing one.
        :param user: The user performing the request
        :return: Post request with an extra data attribute
        """
        data = {
            "author": self.user.id,  # The original author, defined in the setUp
            "title": "",
            "content": ""
        }

        request = self.factory.post('/some-url/')
        # The data is kept in an extra data attribute when the permission methods are called.
        request.data = data
        request.user = user
        return request

    def test_has_object_permission_owner(self):
        # User should have full permission over the object if the user is the author
        request = self.factory.get('/some-url/')
        request.user = self.user
        self.assertTrue(self.permission.has_object_permission(request, "", self.author_object))

    def test_has_object_permission_not_owner(self):
        # User should not have full permission over the object if the user is not the author
        request = self.factory.get('/some-url/')
        request.user = self.other_user
        self.assertFalse(self.permission.has_object_permission(request, "", self.author_object))

    def test_has_permission_owner(self):
        # User should be the author of the object and to be able to have full list
        # permissions.
        request = self.post_request(self.user)
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_not_owner(self):
        # User is not the author of the object and not to be able to have list
        # permissions.

        request = self.post_request(self.other_user)
        self.assertFalse(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_user(self):
        # Because everybody should be able to have read access
        request = self.factory.get('/some-url/')
        request.user = self.user
        self.assertTrue(self.permission.has_permission(request, ""))

    def test_has_permission_get_true_other_user(self):
        # Because everybody should be able to have read access, not just the user that
        # is the author
        request = self.factory.get('/some-url/')
        request.user = self.other_user
        self.assertTrue(self.permission.has_permission(request, ""))
