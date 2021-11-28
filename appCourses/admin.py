from django.contrib import admin
from .models import Course,Assignment,AssignmentSubmission,RegisterCourse

# Register your models here.
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(RegisterCourse)