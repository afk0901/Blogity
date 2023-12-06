from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Posts.views import PostViewSet, CommentViewSet
from rest_framework_nested import routers

router = DefaultRouter()
router.register("", PostViewSet, basename="posts")


posts_router = routers.NestedSimpleRouter(router, "", lookup="post")
posts_router.register("comments", CommentViewSet, basename="posts-comments")


urlpatterns = router.urls + posts_router.urls
