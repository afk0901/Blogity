"""This module defines view-sets for handling CRUD operations for Post and
Comment models.

Features include:
- CRUD operations for posts and comments with custom permission handling.
- Filtering posts by title using DjangoFilterBackend.
- Optionally include related comments in the response with
  the include_comments=True query parameter.
- Filtering comments based on their associated post-ID.
"""

from typing import Type

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from Permissions.author_permissions import IsAuthorAnyRead
from Posts.models import Comment, Post
from Posts.serializers import (
    CommentSerializer,
    PostSerializer,
    PostWithCommentsSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """Viewset for viewing and editing post instances.

    Supports filtering by title, and dynamically returns
    either basic post-information or posts with their related
    comments based on the 'include_comments' query parameter.

    Attributes:
        filter_backends (tuple): DjangoFilterBackend for filtering resources.
        filterset_fields (tuple): Field names allowed for filtering.
        http_method_names (list): Allowed HTTP methods.
        permission_classes (list): Custom permission classes applied to the viewset.
    """

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("title",)
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthorAnyRead]

    def get_serializer_class(
        self,
    ) -> Type[PostWithCommentsSerializer | PostSerializer]:
        """Determine which serializer class to use based on client request.

        Returns:
            PostWithCommentsSerializer or PostSerializer:
            The serializer class for posts,
            including or excluding comments based on
            the request query parameters.
        """
        if self.request.query_params.get("include_comments") == "true":
            return PostWithCommentsSerializer
        return PostSerializer

    def get_queryset(self) -> QuerySet["Post"]:
        """Retrieve the queryset of posts.

        Optionally including related comments
        based on the 'include_comments' query parameter.

        Returns:
            QuerySet["Post"]: A queryset of Post instances,
                              optionally including related comments.
        """
        if self.request.query_params.get("include_comments") == "true":
            return Post.post_manager.get_all_posts_and_related_comments()
        return Post.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing comment instances, filtered by their
    associated post-ID.

    Attributes:
        serializer_class (Type[CommentSerializer]): The serializer class for comments.
        http_method_names (list): Allowed HTTP methods.
        permission_classes (list): Custom permission classes applied to the viewset.
    """

    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthorAnyRead]

    def get_queryset(self) -> QuerySet["Comment"]:
        """Retrieve the queryset of comments for a specific post, identified by
        'post_pk' URL parameter.

        Returns:
            QuerySet["Comment"]: A queryset of Comment instances
                                 associated with the specified post.
        """
        post_id = str(self.kwargs.get("post_pk"))
        return Comment.objects.filter(post_id=post_id)
