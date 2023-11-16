from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Posts.views import PostViewSet, CommentViewSet
from rest_framework_nested import routers

router = DefaultRouter()
# Registering with an empty prefix since it's the main resource of this app's URLs.
router.register("", PostViewSet, basename="posts")


posts_router = routers.NestedSimpleRouter(router, "", lookup="posts")
posts_router.register("comments", CommentViewSet, basename="posts-comments")


urlpatterns = router.urls + posts_router.urls
