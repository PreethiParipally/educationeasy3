from django.urls import reverse
from django.utils.text import slugify

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()


from appCourses.models import Course

# Create your models here.

class Schedule(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  date = models.DateField(default=timezone.now)
  start_time = models.TimeField()
  end_time = models.TimeField()
  vaccine_dose = models.IntegerField()
  seats = models.IntegerField()
  students_per_row = models.IntegerField(default=0)
  class Meta:
    unique_together = ["course", "date", "start_time", "end_time"]

  def __str__(self):
    return self.course.course_name + " by " + self.user.username
  
  def get_html_url(self):
    # print("heo")
    url = reverse('schedular:view_created_schedule', args=(self.course.id,self.pk))
    # print("hello")
    return f'<a  href="{url}" class="event-link" > {self.course} from {self.start_time} to {self.end_time} </a>'
    

class UserBook(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='bookings')
  name = models.CharField(max_length=50,default="")
  vaccine_dose = models.IntegerField()
  # vaccine_certificate = models.FileField()
  seat = models.IntegerField()

  def get_html_url(self):
    # print("heo")
    url = reverse('schedular:view_schedule', args=(self.course.id,self.schedule.pk))
    # print("hello")
    return f'<a  href="{url}" class="event-link" > {self.course} by {self.schedule.user} from {self.schedule.start_time} to {self.schedule.end_time} </a>'

    