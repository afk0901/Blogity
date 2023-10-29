from django.db import models
from Users.models import CustomUser
from .Post import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="users"
    )
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment published on {self.publish_date}"
