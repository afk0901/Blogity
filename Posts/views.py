from rest_framework import viewsets
from Posts.models.Post import Post
from Posts.models.Comment import Comment
from .serializers.PostSerializer import PostSerializer, PostWithCommentsSerializer
from .serializers.CommentSerializer import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    # Using Django filter backend to make queryset filtering available

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id", "title", "author__username", "author")
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        # Switching serializers depending on if include_comments query parameter
        # is present or not
        if self.request.query_params.get("include_comments") == "true":
            return PostWithCommentsSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.query_params.get("include_comments") == "true":
            # Using a custom manager for re-usability without creating maintenance, mess
            # because we need to put in a parameter according to a field.
            return Post.post_manager.get_all_posts_and_related_comments()
        return Post.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
