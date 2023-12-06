from rest_framework import serializers
from Posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "post", "content", "publish_date"]


class PostWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "publish_date", "comments"]
