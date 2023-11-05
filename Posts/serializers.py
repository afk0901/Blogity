from rest_framework import serializers
from Posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "publish_date"]


# Serializes all posts with their related comments
class PostWithCommentsSerializer(serializers.ModelSerializer):
    # Readonly because if a consumer wants to create posts or comments, it would do it on /posts or /comments endpoints

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "publish_date", "comments"]
