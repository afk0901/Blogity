"""/api/users/ URL Configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from Users.views import UserViewSet

router = DefaultRouter()
# Registering with an empty prefix since it's the main resource of this app's URLs.
router.register("", UserViewSet)

urlpatterns = [path("", include(router.urls))]
