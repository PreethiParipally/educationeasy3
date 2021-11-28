from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'appCourses'
urlpatterns=[

    path('courses/',views.viewCourses,name='courses'),
    path('course-view/<int:pk>',views.CourseDetailView, name='course-view'),
    path('create/',views.CreateCourse.as_view(), name='create'),
    path('update/<int:pk>',views.UpdateCourse.as_view(), name='update'),
    path('delete/<int:pk>',views.DeleteCourse.as_view(), name='delete'),
    path('mycreatedcourses/',views.ListCreatedCourses.as_view(), name='mycreatedcourses'),
    path('register_course/<int:id>',views.RegisterCourseView.as_view(),name="register_course"),
    path('my_registered_courses/',views.ListRegisteredCourses.as_view(), name='my_registered_courses'),
    
    path('course/<int:id>/assignments/',views.ListCourseAssignments.as_view(),name='assignments'),    
    path('course/<int:id>/add_assignment/',views.AddAssignment.as_view(), name='add_assignment'),
    path('course/<int:id>/update_assignment/<int:pk>/',views.UpdateAssignment.as_view(), name='update_assignment'),
    path('course/<int:id>/delete_assignment/<int:pk>/',views.DeleteAssignment.as_view(), name='delete_assignment'),

    path('<int:id>/view_assignment/<int:pk>',views.AssignmentDetailView, name='view_assignment'),
    path('course/<int:id1>/assignment/<int:id2>/assignmentsubmissions/',views.viewAssignmentSubmissions.as_view(),name='assignment_submissions'),
    path('course/<int:id1>/assignment/<int:id2>/myassignmentsubmission/',views.viewMyAssignmentSubmission.as_view(),name='my_assignment_submission'),
    path('course/<int:id1>/assignment/<int:id2>/submit_assignment/',views.AddAssignmentSubmissionView.as_view(), name='add_assignment_submission'),
    path('course/<int:id1>/assignment/<int:id2>/update_assignment_submission/<int:pk>/',views.UpdateAssignmentSubmission.as_view(), name='update_assignment_submission'),
    path('course/<int:id1>/assignment/<int:id2>/delete_assignment_submission/<int:pk>/',views.DeleteAssignmentSubmission.as_view(), name='delete_assignment_submission'),

    path('course/<int:id>/resources/',views.ListCourseResources.as_view(),name='resources'),    
    path('course/<int:id>/add_resource/',views.AddResource.as_view(), name='add_resource'),
    path('course/<int:id>/delete_resource/<int:pk>/',views.DeleteResource.as_view(), name='delete_resource'),

    path('search_courses', views.search_courses, name='search_courses'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
