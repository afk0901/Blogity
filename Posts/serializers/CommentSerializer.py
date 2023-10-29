from rest_framework import serializers
from Posts.models.Comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'publish_date']
