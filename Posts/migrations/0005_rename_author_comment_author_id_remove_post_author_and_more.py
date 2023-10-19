# Generated by Django 4.2.6 on 2024-01-14 23:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Posts", "0004_comment_author"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="author",
            new_name="author_id",
        ),
        migrations.RemoveField(
            model_name="post",
            name="author",
        ),
        migrations.AddField(
            model_name="post",
            name="author_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_id",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
