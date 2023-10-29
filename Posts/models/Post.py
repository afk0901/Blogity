from django.db import models

from Posts.managers.PostManager import PostManager
from Users.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="author"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    post_manager = PostManager()

    def __str__(self):
        return f"{self.title} published on {self.publish_date}"
