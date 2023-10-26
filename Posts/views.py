from rest_framework import viewsets
from .models import Post, Comment
from .serializers.PostSerializer import PostSerializer, PostWithCommentsSerializer
from .serializers.CommentSerializer import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ("id", "title", "author__username",)

    def get_serializer_class(self):
        if self.request.query_params.get('include_comments') == 'true':
            return PostWithCommentsSerializer
        return PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('comments') == 'true':
            queryset = queryset.prefetch_related('comment_set')
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
