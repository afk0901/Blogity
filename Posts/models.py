from typing import Never

from django.db import models
from django.db.models import ForeignKey, CharField, TextField, DateTimeField

from Users.models import CustomUser
from django.db.models.query import QuerySet


class PostManager(models.Manager['Post']):
    def get_all_posts_and_related_comments(self) -> QuerySet['Post']:
        # If the field changes, we just change it here.
        return self.all().prefetch_related("comments")


class Post(models.Model):
    author_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    post_manager = PostManager()

    def __str__(self) -> str:
        return f"{self.title} published on {self.publish_date}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Comment published on {self.publish_date}"
