from django.db import models
from django.db.models.fields import related
from django.conf import settings
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    message =  RichTextField(blank=True,null=True)
    message_html = models.TextField(editable=False)
    rank = models.IntegerField(default=0)
    is_pin = models.BooleanField(default=False)
    views= models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    favourite = models.ManyToManyField(User, related_name='favorite', blank=True)
    pdf = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def total_likes(self):
        return self.likes.count()
    def total_views(self):
        return self.views.count()

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']

class Comment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True ,related_name='reply')
    timestamp= models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
