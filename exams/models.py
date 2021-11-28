from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

from appCourses.models import Course

class Exam(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  exam_name = models.CharField(max_length=50)
  def __str__(self):
    return self.exam_name

class Question(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  exam=models.ForeignKey(Exam,on_delete=models.CASCADE,related_name='questions')
  marks=models.PositiveIntegerField()
  question=models.TextField()
  option1=models.CharField(max_length=200)
  option2=models.CharField(max_length=200)
  option3=models.CharField(max_length=200)
  option4=models.CharField(max_length=200)
  cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
  answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
  time_taken = models.PositiveIntegerField(null=True, default=0)
  marks = models.PositiveIntegerField()
  actual_marks = models.PositiveIntegerField(default=0)
  correct = models.PositiveIntegerField(default=0)
  wrong = models.PositiveIntegerField(default=0)
  percent = models.PositiveIntegerField(default=0)
  date = models.DateTimeField(auto_now=True)
