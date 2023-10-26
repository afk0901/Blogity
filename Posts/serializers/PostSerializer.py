from rest_framework import serializers
from Posts.models import Post
from Posts.serializers.CommentSerializer import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content']


class PostWithCommentsSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, source='comment_set', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'publish_date', 'comments']
