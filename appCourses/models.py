from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='media')
    faculty_details = models.TextField()
    course_description = models.TextField()
    created_at = models.DateField(default=timezone.now)
    start_date= models.DateField(default=timezone.now)
    end_date= models.DateField(default=timezone.now)
    def __str__(self):
        return self.course_name
    def __unicode__(self):
        return "".join(self.course_name, " by ", self.user)
    class Meta:
        ordering=['created_at']
        
class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True)

class Assignment(models.Model):
    user = models.ForeignKey(User, related_name='user_assignments', on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE,related_name='assignments')
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "".join(self.title)
        
    class Meta:
        ordering=['created_at']



class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, related_name='user_assignment_submissions', on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE,related_name='course_assignment_submission')
    assignment= models.ForeignKey(Assignment, on_delete=models.CASCADE,related_name='assignment_submission')
    name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    date_submitted = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.assignment.__str__()+" "+  self.name

    class Meta:
        ordering = ['-date_submitted']

class RegisterCourse(models.Model):
    user = models.ForeignKey(User,related_name="userregister",on_delete=models.CASCADE)
    course= models.ForeignKey(Course,related_name="courseregister",on_delete=models.CASCADE)
    date_of_registering=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return "{}_{}".format(self.user.__str__(), self.course.__str__())
    def __unicode__(self):
        return "".join(self.course.__str__(), " by ", self.user)



