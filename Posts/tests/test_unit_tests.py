from django.test import SimpleTestCase
from Posts.views import PostViewSet
from Posts.serializers import PostWithCommentsSerializer, PostSerializer
from unittest.mock import patch


class PostSerializerTest(SimpleTestCase):

    def setUp(self):
        self.mock_request = type('MockRequest', (), {})()
        self.viewset = PostViewSet()
        self.viewset.request = self.mock_request

    def test_get_serializer_class_return_post_serializer(self):
        # Test without the include_comments query param
        self.mock_request.query_params = {}
        self.assertEqual(self.viewset.get_serializer_class(), PostSerializer)

    def test_get_serializer_class_return_post_with_comments_serializer(self):
        # Assert the correct serializer class is returned
        self.mock_request.query_params = {'include_comments': 'true'}
        self.assertEqual(self.viewset.get_serializer_class(), PostWithCommentsSerializer)


class PostQuerySetTest(SimpleTestCase):

    def setUp(self):
        self.viewset = PostViewSet()
        self.viewset.request = type('MockRequest', (), {})()

    @patch('Posts.models.Post.post_manager.get_all_posts_and_related_comments')
    def test_get_queryset_return_related_comments(self, mock_get_all_posts_and_related_comments):
        self.viewset.request.query_params = {'include_comments': 'true'}
        self.viewset.get_queryset()
        mock_get_all_posts_and_related_comments.assert_called_once()

    @patch('Posts.models.Post.objects.all')
    def test_get_queryset_return_all_posts(self, mock_objects_all):
        mock_objects_all.reset_mock()
        self.viewset.request.query_params = {}

        self.viewset.get_queryset()
        mock_objects_all.assert_called_once()
