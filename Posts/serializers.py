"""This module defines serializers for the `Post` and `Comment` models.

It includes serializers for individual `Post` and `Comment` instances,
as well as a serializer that combines posts with their associated
comments for nested serialization.
"""

from rest_framework import serializers

from Posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model instances."""

    class Meta:
        """Defines fields for the Post model."""

        model = Post
        fields = ["id", "author_id", "title", "content"]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model instances."""

    class Meta:
        """Defines fields for the Comment model."""

        model = Comment
        fields = ["id", "author_id", "post", "content", "publish_date"]


class PostWithCommentsSerializer(serializers.ModelSerializer):
    """Composite serializer for Post model instances that include related
    comments."""

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        """Defines fields for the Post model with comments."""

        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_id",
            "publish_date",
            "comments",
        ]
