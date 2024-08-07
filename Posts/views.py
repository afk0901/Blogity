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
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets

from Permissions.author_permissions import IsAuthorAnyRead
from Posts.models import Comment, Post
from Posts.serializers import (
    CommentSerializer,
    PostSerializer,
    PostWithCommentsSerializer,
)


@extend_schema(
    methods=["GET"], description="Retrieve a list of posts or a specific post by ID"
)
@extend_schema(
    methods=["POST"], description="Create a specific post and add the post to the list"
)
@extend_schema(methods=["DELETE"], description="Delete a specific post")
@extend_schema(methods=["PUT"], description="Update a specific post")
@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="include_comments",
            type=OpenApiTypes.BOOL,
            description="Include comments for each post if set to true. "
            "Only available at api/posts/ endpoint.",
            required=False,
        )
    ],
)
class PostViewSet(viewsets.ModelViewSet):
    """Endpoint for viewing and editing posts."""

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

    def get_queryset(self) -> QuerySet:
        """Retrieve the queryset of posts.

        Optionally including related comments
        based on the 'include_comments' query parameter.

        Returns:
            QuerySet: A queryset of Post instances,
                              optionally including related comments.
        """
        if self.request.query_params.get("include_comments") == "true":
            return Post.post_manager.get_all_posts_and_related_comments()
        return Post.objects.all()


@extend_schema(
    methods=["GET"],
    description="Retrieve a list of comments by post ID"
    "or a specific comment by a post ID and then a comment ID",
)
@extend_schema(
    methods=["POST"],
    description="Create a specific comment for a specific post",
)
@extend_schema(
    methods=["DELETE"],
    description="Delete a specific comment for a specific post",
)
@extend_schema(
    methods=["PUT"],
    description="Update a specific comment for a specific post",
)
class CommentViewSet(viewsets.ModelViewSet):
    """Endpoint for viewing and editing comments."""

    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthorAnyRead]

    def get_queryset(self) -> QuerySet:
        """Retrieve the queryset of comments for a specific post, identified by
        'post_pk' URL parameter.

        Returns:
            QuerySet: A queryset of Comment instances
                                 associated with the specified post.
        """
        post_id = str(self.kwargs.get("post_pk"))
        return Comment.objects.filter(post_id=post_id)
