from http import HTTPStatus

from parameterized import parameterized_class
from django.test import TestCase

from Posts.tests.test_end_to_end import TestBlogPost
from rest_framework.test import APIClient

from Posts.models import Post

"""
As the test class itself is parameterized, we put it in a separate file
to simplify running the whole class instead of bounce of other things
just to run the parameterized tests.
It's needed to run these tests from the command line. This is a tradeoff so we can avoid repetition.
"""


@parameterized_class(('authenticate'), [
    (True,),
    (False,),
])
class CreateUserAndGetIndividualPostSuccessfullyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        authenticated_client = TestBlogPost.create_test_user_and_create_blog_post()["authenticated_client"]
        # Different client depending on if we want to make a get request with authorized one or not.
        if cls.authenticate:
            client = authenticated_client
        else:
            client = APIClient()
        post_id = Post.objects.last().id
        cls.response = client.get(f'/api/posts/{post_id}/')

    def test_post_retrieved_successfully_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_post_retrieved_successfully(self):
        self.assertContains(self.response, "author_id")
        self.assertContains(self.response, "title")
        self.assertContains(self.response, "content")
