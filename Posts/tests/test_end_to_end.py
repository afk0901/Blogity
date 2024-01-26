from django.forms import model_to_dict
from django.test import TestCase

from Posts.models import Post, Comment
from Users.models import CustomUser
from Users.tests import TestUser
from rest_framework.test import APIClient
import json
from http import HTTPStatus
from parameterized import parameterized_class
from model_bakery import baker

"""
This test suite tests the PostViewSet.
Using setUpClass because we don't want to create a new
record in the test database many times which may create
problems.
"""


class TestBlogPost:
    @staticmethod
    def setup_user_posts_and_client(authenticate_client: bool, number_of_posts=1):
        """
        Will always create a blog post with authenticated user.
        Returns authenticated client or not authenticated client
        depending on the authnticate paramater.

        :param authenticate: If we should return authenticated client or not.
        :param number_of_posts:
        :return:
        """
        authenticated_client = TestBlogPost.create_test_user_and_create_blog_post(number_of_posts=number_of_posts)[
            "authenticated_client"]
        client = authenticated_client if authenticate_client else APIClient()
        return client

    @staticmethod
    def create_test_blog_post_request_data_and_response(client: APIClient, user: CustomUser, number_of_posts=1):
        # Request data and response array are arranged in the same order as the requests are made.
        request_data_responses = []

        for request_data in range(0, number_of_posts):
            request_data = model_to_dict(baker.prepare(Post, author_id=user))
            response = client.post('/api/posts/', data=request_data, format='json')
            request_data_responses.append({"request_data": request_data, "response": response})
        return request_data_responses

    @staticmethod
    def create_test_user_and_create_blog_post(number_of_posts=1):
        """
        Creates a new user, authenticates the user and creates a blog post.
        :return: Dict of request data and response post created by an authenticated user - {'request_data', 'response'}
        """
        user_and_client = TestUser.create_authenticated_test_user()
        user = user_and_client["custom_user_instance"]
        authenticated_client = user_and_client["authenticated_client"]

        request_data_and_responses = TestBlogPost.create_test_blog_post_request_data_and_response(authenticated_client,
                                                                                                  user,
                                                                                                  number_of_posts)

        return {"request_data_responses": request_data_and_responses,
                "authenticated_client": authenticated_client}


class TestBlogComment:

    @staticmethod
    def create_comment_post_response(client: APIClient, post: Post, user: CustomUser, comment_id: int):
        comment = model_to_dict(baker.prepare(Comment,
                                              id=comment_id,
                                              post=post,
                                              author_id=user,
                                              content="Test comment"))

        client.post(f'/api/posts/1/comments/', data=comment, format='json')



class AuthenticatedUserCreatedPostSuccessfullyTest(TestCase):

    def setUp(self):
        created_post_with_authenticated_user_request_response = (TestBlogPost.
                                                                 create_test_user_and_create_blog_post())[
            "request_data_responses"]
        self.response = created_post_with_authenticated_user_request_response[0]["response"]
        self.response_data = self.response.data
        self.request_data = created_post_with_authenticated_user_request_response[0]["request_data"]

    def test_post_created_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_post_created_successfully(self):
        self.assertEqual(self.request_data["author_id"], self.response_data["author_id"])
        self.assertEqual(self.request_data["title"], self.response_data["title"])
        self.assertEqual(self.request_data["content"], self.response_data["content"])


class AuthenticatedUserCreatedUpdatedIndividualPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user_and_create_blog_post = TestBlogPost.create_test_user_and_create_blog_post()
        request_data_response = create_test_user_and_create_blog_post["request_data_responses"]
        post_id = Post.objects.last().id

        cls.request_data = request_data_response[0]["request_data"]
        cls.update_url = f'/api/posts/{post_id}/'
        cls.update_client = create_test_user_and_create_blog_post["authenticated_client"]

    def test_update_title(self):
        request_data = self.request_data.copy()
        request_data["title"] = "Updated title"
        response = self.update_client.put(self.update_url, data=json.dumps(request_data),
                                          content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(self.request_data["title"], response.data["title"])

    def test_update_content(self):
        request_data = self.request_data.copy()
        request_data["content"] = "Updated content"
        response = self.update_client.put(self.update_url, data=json.dumps(request_data),
                                          content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(self.request_data["content"], response.data["content"])


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserAndGetIndividualPostSuccessfullyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = TestBlogPost.setup_user_posts_and_client(cls.authenticate)
        post_id = Post.objects.last().id
        cls.response = client.get(f'/api/posts/{post_id}/')

    def test_post_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_post_retrieved_successfully(self):
        self.assertContains(self.response, "author_id")
        self.assertContains(self.response, "title")
        self.assertContains(self.response, "content")


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserAndGetAllPostsTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        client = TestBlogPost.setup_user_posts_and_client(cls.authenticate, number_of_posts=3)
        p = Post.objects.all()
        cls.response = client.get(f'/api/posts/')

    def test_post_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_post_retrieved_successfully(self):
        self.assertEqual(len(self.response.data), 3)

        for post in self.response.data:
            self.assertIn("author_id", post)
            self.assertIn("title", post)
            self.assertIn("content", post)


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserAndGetAllCommentsRelatedToPostTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Post.objects.all().delete()
        client = TestBlogPost.setup_user_posts_and_client(True, number_of_posts=1)
        post = Post.objects.last()
        user = baker.prepare(CustomUser, id=CustomUser.objects.last().id)
        TestBlogComment.create_comment_post_response(client, post, user, 1)
        cls.response = client.get(f'/api/posts/{post.id}/comments/')


    def test_comment_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_comment_retrieved_successfully(self):
        self.assertEqual(len(self.response.data), 1)

        for comment in self.response.data:
            self.assertIn("author_id", comment)
            self.assertIn("post", comment)
            self.assertIn("content", comment)
