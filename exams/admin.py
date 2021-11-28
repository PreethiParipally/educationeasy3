from django.contrib import admin
from .models import Exam,Question,Result

# Register your models here.
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Result)