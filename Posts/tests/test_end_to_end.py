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

from Authentication.client import Client

"""
This test suite tests the PostViewSet.
Using setUpClass because we don't want to create a new
record in the test database many times which may create
problems.
"""


class TestBlogPost:
    @staticmethod
    def setup_user_posts_and_client(authenticate_client: bool, number_of_posts=1) -> APIClient:
        """
        Will always create a blog post with authenticated user.

        :param authenticate_client: If we should return an authenticated client or not.
        :param number_of_posts: Number of posts to be generated with a POST request.
        :return: client.
        """
        authenticated_client = TestBlogPost.create_test_user_and_create_blog_post(number_of_posts=number_of_posts)[
            "authenticated_client"]
        client = Client.get_client(authenticated_client, authenticate_client)
        return client

    @staticmethod
    def setup_user_posts_get_authenticated_client_and_post_id(authenticate_client: bool, number_of_posts=1):
        """
        Sets up blog post and the authenticated client if we want the client to be authenticated.
        :param number_of_posts: Number of blog posts.
        :param authenticate_client: Should it return an authenticated client or not?
        :return: Tuple of a client and post
        """
        # To create posts, we need to be authenticated so that's why hardcoded to true.
        authenticated_client = TestBlogPost.setup_user_posts_and_client(True, number_of_posts)
        client = Client.get_client(authenticated_client, authenticate_client)
        last_post = Post.objects.last()
        return client, last_post, authenticated_client

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
        user_and_client = TestUser.create_test_user()
        user = user_and_client["custom_user_instance"]
        authenticated_client = user_and_client["authenticated_client"]

        request_data_and_responses = TestBlogPost.create_test_blog_post_request_data_and_response(authenticated_client,
                                                                                                  user,
                                                                                                  number_of_posts)

        return {"request_data_responses": request_data_and_responses,
                "authenticated_client": authenticated_client}


class TestBlogComment:

    @staticmethod
    def create_comment_post_response(client: APIClient,
                                     post: Post,
                                     number_of_comments=1):
        user = baker.prepare(CustomUser, id=CustomUser.objects.last().id)
        post_id = post.id
        request_data_and_responses = []

        for _ in range(number_of_comments):
            comment = model_to_dict(baker.prepare(Comment,
                                                  post=post,
                                                  author_id=user
                                                  ))

            request_data_and_response = {"request_data": comment,
                                         "response": client.post(f'/api/posts/{post_id}/comments/',
                                                                 data=comment, format='json')}
            request_data_and_responses.append(request_data_and_response)

        return request_data_and_responses

    @staticmethod
    def setup_user_posts_get_authenticated_user_create_comment_client_post(authenticate: bool, number_of_comments=1):
        client_and_post_id = TestBlogPost.setup_user_posts_get_authenticated_client_and_post_id(authenticate)
        authenticated_client = client_and_post_id[2]
        client = client_and_post_id[0]
        post = client_and_post_id[1]
        TestBlogComment.create_comment_post_response(authenticated_client, post, number_of_comments)
        return client, post


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
        cls.post_id = Post.objects.last().id

        cls.request_data = request_data_response[0]["request_data"]
        cls.update_url = f'/api/posts/{cls.post_id}/'
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

    def test_only_owner_can_update(self):
        updated_user_response = TestUser.create_test_user()["authenticated_client"].put(self.update_url,
                                                                                        data=json.dumps(
                                                                                            self.request_data),
                                                                                        content_type='application/json')

        self.assertEqual(updated_user_response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthorized_user_cant_update(self):
        user = baker.prepare(CustomUser, id=1)
        data = model_to_dict(baker.prepare(Post, id=1, author_id=user))
        resp = APIClient().put(f'/api/posts/{self.post_id}/', data=json.dumps(data),
                                                                    content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


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

    def test_unauthorized_user_cant_create_post_status_code(self):
        user = baker.prepare(CustomUser, id=1)
        data = model_to_dict(baker.prepare(Post, id=1, author_id=user))
        resp = APIClient().post(f'/api/posts/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserAndGetAllPostsTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        client = TestBlogPost.setup_user_posts_and_client(cls.authenticate, number_of_posts=3)
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
        client, post = TestBlogComment.setup_user_posts_get_authenticated_user_create_comment_client_post(
            authenticate=
            cls.authenticate,
            number_of_comments=3)
        cls.response = client.get(f'/api/posts/{post.id}/comments/')

    def test_comment_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_comment_retrieved_successfully(self):
        self.assertEqual(len(self.response.data), 3)

        for comment in self.response.data:
            self.assertIn("author_id", comment)
            self.assertIn("post", comment)
            self.assertIn("content", comment)


class CreateUserCreatePostCreateComments(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # To create posts, we need to be authenticated so that's why hardcoded to true.
        authenticated_client = TestBlogPost.setup_user_posts_and_client(True, number_of_posts=1)
        post = Post.objects.last()
        response_and_request_data = TestBlogComment.create_comment_post_response(authenticated_client, post,
                                                                                 number_of_comments=1)[0]
        cls.response = response_and_request_data["response"]
        cls.request_data = response_and_request_data["request_data"]
        cls.response_data = response_and_request_data["response"].data

    def test_comment_created_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.CREATED)

    def test_comment_created_successfully(self):
        self.assertEqual(self.request_data["author_id"], self.response_data["author_id"])
        self.assertEqual(self.request_data["post"], self.response_data["post"])
        self.assertEqual(self.request_data["content"], self.response_data["content"])

    def test_unauthorized_user_cant_create(self):
        user = baker.prepare(CustomUser, id=1)
        post_id = self.request_data["post"]
        data = model_to_dict(baker.prepare(Comment, id=1, author_id=user))
        resp = APIClient().post(f"/api/posts/{post_id}/comments/", data=json.dumps(data),
                                                                        content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserCreatePostCreateCommentGetIndividualComment(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        client, post = TestBlogComment.setup_user_posts_get_authenticated_user_create_comment_client_post(
            cls.authenticate)
        comment_id = Comment.objects.filter(post=post)[0].id
        cls.response = client.get(f'/api/posts/{post.id}/comments/{comment_id}/')

    def test_comment_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_comment_retrieved_successfully(self):
        self.assertContains(self.response, "id")
        self.assertContains(self.response, "author_id")
        self.assertContains(self.response, "content")


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserCreatePostCreateCommentGetAllCommentsAndAllPosts(TestCase):
    @classmethod
    def setUpTestData(cls):
        client_and_post_id = TestBlogPost.setup_user_posts_get_authenticated_client_and_post_id(cls.authenticate,
                                                                                                number_of_posts=3)
        authenticated_client = client_and_post_id[2]
        client = client_and_post_id[0]
        for post in Post.objects.all():
            TestBlogComment.create_comment_post_response(authenticated_client, post, number_of_comments=1)
        cls.response = client.get(f'/api/posts/?include_comments=true')

    def test_all_posts_and_comments_fetched_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_all_posts_and_comments_fetched_successfully(self):
        self.assertEqual(len(self.response.data), 3)

        for post in self.response.data:
            self.assertIn("author_id", post)
            self.assertIn("title", post)
            self.assertIn("content", post)

            comment = post["comments"][0]
            self.assertIn("author_id", comment)
            self.assertIn("post", comment)
            self.assertIn("content", comment)


class CreateUserCreatePostCreateCommentUpdateIndividualComment(TestCase):

    @classmethod
    def setUpTestData(cls):
        client, post = TestBlogComment.setup_user_posts_get_authenticated_user_create_comment_client_post(
            authenticate=True)
        comment_id = Comment.objects.last().id
        cls.old_comment = client.get(f'/api/posts/{post.id}/comments/{comment_id}/')
        author = baker.prepare(CustomUser, id=cls.old_comment.data["author_id"])
        cls.new_comment = model_to_dict(baker.prepare(Comment, id=1, post=post, author_id=author))
        cls.update_url = f'/api/posts/{post.id}/comments/{comment_id}/'
        cls.updated_comment_response = client.put(cls.update_url, data=json.dumps(cls.new_comment),
                                                                    content_type='application/json')

    def test_update_individual_comment_status_code(self):
        self.assertEqual(self.updated_comment_response.status_code, HTTPStatus.OK)

    def test_update_individual_comment(self):
        self.assertNotEqual(self.updated_comment_response.data["content"], self.old_comment.data["content"])
        self.assertEqual(self.updated_comment_response.data["post"], self.old_comment.data["post"])
        self.assertEqual(self.updated_comment_response.data["content"], self.new_comment["content"])

    def test_only_owner_can_update(self):
        updated_user_response = TestUser.create_test_user()["authenticated_client"].put(self.update_url,
                                                                                        data=json.dumps(
                                                                                            self.new_comment),
                                                                                        content_type='application/json')

        self.assertEqual(updated_user_response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthorized_user_cant_update(self):
        user = baker.prepare(CustomUser, id=1)
        data = model_to_dict(baker.prepare(Comment, id=1, author_id=user))
        resp = APIClient().put(self.update_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)


class CreateUserCreatePostDeletePost(TestCase):

    @classmethod
    def setUpTestData(cls):
        authenticated_client = TestBlogPost.setup_user_posts_and_client(True, number_of_posts=3)
        cls.post_id = Post.objects.last().id
        cls.resp = authenticated_client.delete(f"/api/posts/{cls.post_id}/")

    def test_delete_post_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.NO_CONTENT)

    def test_post_deleted(self):
        post_deleted = not Post.objects.filter(id=self.post_id).exists()
        self.assertTrue(post_deleted)

    def test_only_owner_can_delete(self):
        resp = TestUser.create_test_user()["authenticated_client"].delete(
                                    f"/api/posts/{self.post_id-1}/")

        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)


class CreateUserCreatePostDeleteIndividualComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        client, post = TestBlogComment.setup_user_posts_get_authenticated_user_create_comment_client_post(
            authenticate=True,
            number_of_comments=3)
        cls.last_comment_id = Comment.objects.last().id
        cls.post_id = post.id
        cls.resp = client.delete(f"/api/posts/{cls.post_id}/comments/{cls.last_comment_id}/")

    def test_delete_comment_status(self):
        self.assertEqual(self.resp.status_code, HTTPStatus.NO_CONTENT)

    def test_comment_deleted(self):
        comment_deleted = not Comment.objects.filter(id=self.last_comment_id).exists()
        self.assertTrue(comment_deleted)

    def test_only_owner_can_delete(self):
        resp = TestUser.create_test_user()["authenticated_client"].delete(
                                    f"/api/posts/{self.post_id}/comments/{self.last_comment_id-1}/")

        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthorized_user_cannot_delete(self):
        resp = APIClient().delete(f'/api/posts/{self.post_id}/', content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

    def test_unauthorized_user_cannot_delete_comment(self):
        resp = APIClient().delete(f'/api/posts/{self.post_id}/', content_type="application/json")
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
