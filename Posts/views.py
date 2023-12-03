from rest_framework import viewsets

from Permissions.author_permissions import IsAuthorAnyRead
from Posts.models import Post, Comment
from Posts.serializers import PostSerializer, PostWithCommentsSerializer
from Posts.serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):

    # Using Django filter backend to filter by query-parameters from the URL
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id", "title", "author__username", "author")
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthorAnyRead]

    def get_serializer_class(self):
        # Switching serializers depending on if include_comments query parameter
        # is present or not
        if self.request.query_params.get("include_comments") == "true":
            return PostWithCommentsSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.query_params.get("include_comments") == "true":
            return Post.post_manager.get_all_posts_and_related_comments()
        return Post.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthorAnyRead]
    # Using Django filter backend to filter by query-parameters from the URL
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id", "author__username", "author", "publish_date")
