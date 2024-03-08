"""This module handles posts URLS configuration."""

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from Posts.views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("", PostViewSet, basename="posts")


posts_router = routers.NestedSimpleRouter(router, "", lookup="post")
posts_router.register("comments", CommentViewSet, basename="posts-comments")


urlpatterns = router.urls + posts_router.urls
