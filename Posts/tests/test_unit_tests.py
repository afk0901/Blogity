from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from Posts.serializers import PostSerializer, PostWithCommentsSerializer
from Posts.views import PostViewSet


class PostSerializerTest(SimpleTestCase):
    def setUp(self) -> None:
        self.mock_request = type("MockRequest", (), {})()
        self.viewset = PostViewSet()
        self.viewset.request = self.mock_request

    def test_get_serializer_class_return_post_serializer(self) -> None:
        # Test without the include_comments query param
        self.mock_request.query_params = {}
        self.assertEqual(self.viewset.get_serializer_class(), PostSerializer)

    def test_get_serializer_class_return_post_with_comments_serializer(
        self,
    ) -> None:
        # Assert the correct serializer class is returned
        self.mock_request.query_params = {"include_comments": "true"}
        self.assertEqual(
            self.viewset.get_serializer_class(), PostWithCommentsSerializer
        )


class PostQuerySetTest(SimpleTestCase):
    def setUp(self) -> None:
        self.mock_request = type("MockRequest", (), {})()
        self.viewset = PostViewSet()
        self.viewset.request = self.mock_request

    @patch("Posts.models.Post.post_manager.get_all_posts_and_related_comments")
    def test_get_queryset_return_related_comments(
        self, mock_get_all_posts_and_related_comments: MagicMock
    ) -> None:
        self.mock_request.query_params = {"include_comments": "true"}
        self.viewset.get_queryset()
        mock_get_all_posts_and_related_comments.assert_called_once()

    @patch("Posts.models.Post.objects.all")
    def test_get_queryset_return_all_posts(self, mock_objects_all: MagicMock) -> None:
        self.mock_request.query_params = {}
        self.viewset.get_queryset()
        mock_objects_all.assert_called_once()
