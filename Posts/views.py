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
    """Endpoint for viewing and editing posts.

    Supports filtering by title, and optionally returns related comments for each post.

    Supported methods: GET, POST, PUT, DELETE

    Get Operations:
    - /: Returns a list of all posts in the system.
    - /<id>: Returns a specific post by id

    Post Operations:
    - /: Adds a new post to the system

    Put Operations:
    - /<id>: Updates a specific post

    Delete Operations:
    - /<id>: Deletes a specific post

    Note: Pagination will be implemented in a future update.

    Query Parameters:
    - `title` (optional): Filters posts by title. Usage: `/?title=<title of post>`
    - `include_comments` (optional): Includes comments related to each post in the
       response when set to True.
       Usage: `/?include_comments=True`
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
    """Endpoint for viewing and editing comments.

    Supported methods: GET, POST, PUT, DELETE

    Get Operations:
    - /<post_id>/comments/: Returns a list of all comments for a specific post.
    - /<post_id>/comments/<id>/: Returns a specific comment by id for a specific post

    Post Operations:
    - /: Adds a new comment to the system

    Put Operations:
    - /<post_id><comment_id>/: Updates a specific comment for a specific post

    Delete Operations:
    - /<post_id>/<comment_id>/: Deletes a specific comment for a specific post

    Note: Pagination will be implemented in a future update.

    Query Parameters: None.
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
