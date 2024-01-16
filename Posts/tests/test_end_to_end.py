from django.test import TestCase

from Posts.models import Post
from Users.tests import TestUser
from rest_framework.test import APIClient

"""
This test suite tests the PostViewSet
"""


class TestBlogPost:

    @staticmethod
    def blog_post_test_data(blog_post_author_id):
        """
        :return: Dict of user test data
        """
        return {
            "author_id": blog_post_author_id,
            "title": "Blog post title",
            "content": "Blog post content"
        }

    @staticmethod
    def create_test_user_authenticate_and_create_blog_post():
        """
        Creates a new user, authenticates the user and creates ablog post.
        :return: Dict of request data and response post created by an authenticated user - {'request_data', 'response'}
        """
        user_and_auth_response = TestUser.create_test_user_and_authenticate_response()
        auth_response = user_and_auth_response['response']
        token = auth_response.data['access']
        client = APIClient(headers={"Authorization": "Bearer " + token})

        user_id = user_and_auth_response['user']['id']
        request_data = TestBlogPost.blog_post_test_data(blog_post_author_id=user_id)

        response = client.post('/api/posts/', data=request_data, format='json')
        return {"request_data": request_data, "response": response}


class AuthenticatedUserCreatedPostSuccessfullyTest(TestCase):

    def setUp(self):
        created_post_with_authenticated_user_response_dict = (TestBlogPost.
                                                              create_test_user_authenticate_and_create_blog_post())

        self.response = created_post_with_authenticated_user_response_dict["response"]
        self.response_data = self.response.data
        self.request_data = created_post_with_authenticated_user_response_dict["request_data"]

    def test_post_created_successfully_status_code(self):
        self.assertEqual(self.response.status_code, 201)

    def test_post_created_successfully(self):
        self.assertEqual(self.request_data["author_id"], self.response_data["author_id"])
        self.assertEqual(self.request_data["title"], self.response_data["title"])
        self.assertEqual(self.request_data["content"], self.response_data["content"])


class AuthenticatedUserGetIndividualPostSuccessfullyTest(TestCase):

    # Using setUpClass because we don't want to create a new user many times.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TestBlogPost.create_test_user_authenticate_and_create_blog_post()
        client = APIClient()
        # ID does not necessary start at 1, so taking the last post created.
        post_id = Post.objects.last().id
        cls.response = client.get(f'/api/posts/{post_id}/')

    def test_post_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_retrieved_successfully(self):
        self.assertContains(self.response, "author_id")
        self.assertContains(self.response, "title")
        self.assertContains(self.response, "content")
