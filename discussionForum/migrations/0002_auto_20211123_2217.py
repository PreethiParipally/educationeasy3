# Generated by Django 3.2.9 on 2021-11-23 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussionForum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='post',
            new_name='query',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='upvotes',
        ),
        migrations.RemoveField(
            model_name='query',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='query',
            name='upvotes',
        ),
    ]