"""Defines the models for blog posts and associated comments.

A custom manager for the `Post` model is also provided to optimize
queries for retrieving posts with their comments and to avoid violating
the DRY principle.
"""

from django.db import models
from django.db.models.query import QuerySet

from Users.models import CustomUser


class PostManager(models.Manager):
    """A custom manager for the Post model, adds methods to efficiently query
    all posts and their related comments."""

    def get_all_posts_and_related_comments(self) -> QuerySet:
        """Retrieve all Post instances from the database, prefetching related
        comments to minimize database queries.

        Returns:
            QuerySet: A QuerySet of all Post instances with their related
            comments prefetched.
        """
        return self.all().prefetch_related("comments")


class Post(models.Model):
    """A blog post model representing individual blog entries."""

    author_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    objects = (
        models.Manager()
    )  # In the case, we may not want to use the custom manager.
    post_manager = PostManager()

    def __str__(self) -> str:
        """Return a string representation of the Post instance, including its
        title and publish date."""
        return f"{self.title} published on {self.publish_date}"


class Comment(models.Model):
    """A comment model for blog posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the Comment instance, including
        its publishing date."""
        return f"Comment published on {self.publish_date}"
