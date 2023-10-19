from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from Permissions.user_permissions import UserOnlyModifyOwnAllowRead
from Users.models import CustomUser


class UserOnlyModifyOwnAllowReadTest(SimpleTestCase):
    def setUp(self) -> None:
        self.permission = UserOnlyModifyOwnAllowRead()
        self.factory = APIRequestFactory()
        self.detail_view_url = "/some-url/1/"
        self.data: dict[str, int | str] = {
            "id": 18,
            "username": "admin",
            "first_name": "admin",
            "last_name": "admin",
            "password": "12345",
        }
        self.view = APIView()

    def test_user_has_object_permission_denied_anonymous_user(self) -> None:
        request = self.factory.put(self.detail_view_url, self.data)
        request.user = AnonymousUser()
        self.assertFalse(
            self.permission.has_object_permission(request, self.view, CustomUser())
        )

    def test_user_has_object_permission_denied_logged_in_user(self) -> None:
        request = self.factory.put(self.detail_view_url, self.data)
        user = Mock()
        request.user = user
        self.assertFalse(
            self.permission.has_object_permission(request, self.view, CustomUser())
        )

    def test_user_has_object_permission_granted(self) -> None:
        user = CustomUser()
        request = self.factory.put(self.detail_view_url, self.data)
        request.user = user
        self.assertTrue(self.permission.has_object_permission(request, self.view, user))

    def test_user_has_object_permission_anonymous_user_granted_to_read(
        self,
    ) -> None:
        request = self.factory.get(self.detail_view_url, self.data)
        request.user = AnonymousUser()
        self.assertTrue(
            self.permission.has_object_permission(request, self.view, CustomUser())
        )

    def test_user_has_object_permission_authenticated_user_granted_to_read(
        self,
    ) -> None:
        request = self.factory.get(self.detail_view_url, self.data)
        request.user = CustomUser()
        self.assertTrue(
            self.permission.has_object_permission(request, self.view, CustomUser())
        )
