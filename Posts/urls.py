from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
# Registering with an empty prefix since it's the main resource of this app's URLs.
router.register('', PostViewSet, basename="posts")

urlpatterns = [

    path('', include(router.urls)),
]
