from django.db import models

from Posts.models import Post


class PostManager(models.Manager):

    def get_all_posts_and_related_comments(self):
        # If the field changes, we just change it here.
        return self.all().prefetch_related('comments')
