from django.test import TestCase
from rest_framework.test import APIRequestFactory
from Permissions.author_permissions import IsAuthor
from Users.models import CustomUser
from unittest.mock import Mock


class CustomPermissionTestCase(TestCase):

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
