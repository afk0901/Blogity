from rest_framework import viewsets

from Permissions.author_permissions import IsAuthorAnyRead
from Posts.models import Post, Comment
from Posts.serializers import PostSerializer, PostWithCommentsSerializer
from Posts.serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("title", )
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthorAnyRead]

    def get_serializer_class(self):
        if self.request.query_params.get("include_comments") == "true":
            return PostWithCommentsSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.query_params.get("include_comments") == "true":
            return Post.post_manager.get_all_posts_and_related_comments()
        return Post.objects.all()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthorAnyRead]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)
