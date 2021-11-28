from django.contrib import admin
from .models import Schedule, UserBook,get_user_model

# Register your models here.
admin.site.register(Schedule)
admin.site.register(UserBook)