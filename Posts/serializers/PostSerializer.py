from rest_framework import serializers
from Posts.models.Post import Post
from Posts.serializers.CommentSerializer import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content"]


class PostWithCommentsSerializer(serializers.ModelSerializer):
    # Readonly because if a consumer wants to create posts or comments, it would do it on /posts or /comments endpoints

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "publish_date", "comments"]
