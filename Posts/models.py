from django.db import models

from Users.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users")
    title = models.CharField(max_length=100)
    content = models.TextField(related_name="content")
    publish_date = models.DateTimeField(auto_now=True, related_name="publish_date")

    def __str__(self):
        return f"{self.title} published on {self.publish_date}"


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users")
    content = models.TextField(related_name="content")
    publish_date = models.DateTimeField(auto_now=True, related_name="publish_date")

    def __str__(self):
        return f"Comment published on {self.publish_date}"
