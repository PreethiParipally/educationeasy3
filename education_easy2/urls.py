"""edublog2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('posts/', include('posts.urls',namespace='posts')),
    path('courses/', include('appCourses.urls',namespace='courses')),
    path('exams/course/', include('exams.urls',namespace='exams')),
    path('discussions/course/', include('discussionForum.urls',namespace='discussions')),
    path('schedular/course/', include('schedular.urls',namespace='schedular')),
    path('calendar/', include('scheduleCalendar.urls',namespace='scheduleCalendar')),
    path('BookingsCalendar/', include('BookingsCalendar.urls',namespace='BookingsCalendar')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)