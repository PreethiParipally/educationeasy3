from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'appCourses'
urlpatterns=[
   
    path('<int:id>/exams/',views.ListFacultyCourseExams.as_view(),name='exams'),
    path('<int:id1>/exams/<int:id2>/view_results',views.view_results,name='view_results'),
    path('<int:id>/add_exam/',views.AddExam.as_view(), name='add_exam'),
    path('<int:id1>/view_exam/<int:id2>/',views.ViewExam.as_view(), name='view_exam'),
    path('<int:id>/update_exam/<int:pk>/',views.UpdateExam.as_view(), name='update_exam'),
    path('<int:id>/delete_exam/<int:pk>/',views.DeleteExam.as_view(), name='delete_exam'),

    path('<int:id1>/exam/<int:id2>/add_question/',views.AddQuestion.as_view(), name='add_question'),
    path('<int:id1>/exam/<int:id2>/update_question/<int:pk>/',views.UpdateQuestion.as_view(), name='update_question'),
    path('<int:id1>/exam/<int:id2>/delete_question/<int:pk>/',views.DeleteQuestion.as_view(), name='delete_question'),

    path('<int:id>/exams_student/',views.ListStudentCourseExams.as_view(),name='exams_student'),
    path('<int:id>/take_exam/<int:pk>', views.take_exam_view,name='take_exam'),
    path('<int:id>/start_exam/<int:pk>', views.start_exam_view,name='start_exam'),

    path('<int:id>/calculate_marks/', views.calculate_marks_view,name='calculate_marks'),
    path('<int:id>/view_result', views.view_result_view,name='view_result'),
    path('<int:id>/check_marks/<int:pk>', views.check_marks_view,name='check_marks'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
