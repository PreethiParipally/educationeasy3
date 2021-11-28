from django.db import models
from django.db.models.fields import related
from django.conf import settings
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from appCourses.models import Course
User = get_user_model()


class Query(models.Model):
    user = models.ForeignKey(User, related_name='queries',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    question =  RichTextField(blank=True,null=True)
    message_html = models.TextField(editable=False)
    rank = models.IntegerField(default=0)
    # upvotes = models.ManyToManyField(User, related_name='upvotes', blank=True)
    # downvotes = models.ManyToManyField(User, related_name='downvotes', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-rank']
        unique_together = ['user','course', 'question']

class Answer(models.Model):
    sno= models.AutoField(primary_key=True)
    answer=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    query=models.ForeignKey(Query, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True ,related_name='reply')
    timestamp= models.DateTimeField(default=timezone.now)
    # upvotes = models.ManyToManyField(User, related_name='a_upvotes', blank=True)
    # downvotes = models.ManyToManyField(User, related_name='a_downvotes', blank=True)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.answer[0:13] + "..." + "by " + self.user.username + " for "+ self.course.course_name+" "+self.query.title
