from django.db import models

from Users.models import CustomUser


class PostManager(models.Manager):
    def get_all_posts_and_related_comments(self):
        # If the field changes, we just change it here.
        return self.all().prefetch_related("comments")


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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="users"
    )
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment published on {self.publish_date}"
