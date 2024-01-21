from django.test import TestCase

from Posts.models import Post
from Users.tests import TestUser
from rest_framework.test import APIClient
import json
from http import HTTPStatus
from parameterized import parameterized_class

"""
This test suite tests the PostViewSet.
Using setUpClass because we don't want to create a new
record in the test database many times which may create
problems.
"""


class TestBlogPost:
    @staticmethod
    def setup_user_post_and_client(authenticate: bool):
        authenticated_client = TestBlogPost.create_test_user_and_create_blog_post()["authenticated_client"]
        client = authenticated_client if authenticate else APIClient()
        return client

    @staticmethod
    def blog_post_test_data(blog_post_author_id: int):
        """
        :return: Dict of blog test data
        """
        return {
            "author_id": blog_post_author_id,
            "title": 'Blog post title',
            "content": 'Blog post content'
        }

    @staticmethod
    def create_test_blog_post_request_data_and_response(client: APIClient, blog_post_author_id: int):
        request_data = TestBlogPost.blog_post_test_data(blog_post_author_id=blog_post_author_id)
        response = client.post('/api/posts/', data=request_data, format='json')
        return {"request_data": request_data, "response": response}

    @staticmethod
    def create_test_user_and_create_blog_post():
        """
        Creates a new user, authenticates the user and creates a blog post.
        :return: Dict of request data and response post created by an authenticated user - {'request_data', 'response'}
        """
        user_and_client = TestUser.create_authenticated_test_user()
        user = user_and_client["user"]
        authenticated_client = user_and_client["authenticated_client"]

        user_id = user['id']

        request_data_and_response = TestBlogPost.create_test_blog_post_request_data_and_response(authenticated_client,
                                                                                                 user_id)

        return {"request_data": request_data_and_response["request_data"],
                "response": request_data_and_response["response"],
                "authenticated_client": authenticated_client}


class AuthenticatedUserCreatedPostSuccessfullyTest(TestCase):

    def setUp(self):
        created_post_with_authenticated_user_response_dict = (TestBlogPost.
                                                              create_test_user_and_create_blog_post())
        self.response = created_post_with_authenticated_user_response_dict["response"]
        self.response_data = self.response.data
        self.request_data = created_post_with_authenticated_user_response_dict["request_data"]

    def test_post_created_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_post_created_successfully(self):
        self.assertEqual(self.request_data["author_id"], self.response_data["author_id"])
        self.assertEqual(self.request_data["title"], self.response_data["title"])
        self.assertEqual(self.request_data["content"], self.response_data["content"])


class AuthenticatedUserCreatedUpdatedIndividualPost(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_user_and_create_blog_post = TestBlogPost.create_test_user_and_create_blog_post()
        post_id = Post.objects.last().id

        cls.request_data = create_test_user_and_create_blog_post["request_data"]
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
        client = TestBlogPost.setup_user_post_and_client(cls.authenticate)
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
        client = TestBlogPost.setup_user_post_and_client(cls.authenticate)

        cls.response = client.get(f'/api/posts/')

    def test_post_retrieved_successfully_status_code(self):
        ...
    #     self.assertEqual(self.response.status_code, HTTPStatus.OK)
    #
    # def test_post_retrieved_successfully(self):
    #     self.assertContains(self.response[], "author_id")
    #     self.assertContains(self.response, "title")
    #     self.assertContains(self.response, "content")
