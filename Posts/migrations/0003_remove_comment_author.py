# Generated by Django 4.2.6 on 2023-11-06 01:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Posts", "0002_comment_delete_comments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="author",
        ),
    ]
