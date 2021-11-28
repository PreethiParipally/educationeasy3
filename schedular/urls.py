from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='schedular'

urlpatterns = [
    path('my_schedules/', views.ViewMySchedules.as_view(), name='my_schedules'),

    path('<int:id>/schedules/', views.ViewSchedules.as_view(), name='schedules'),
    path('<int:id>/view_created_schedule/<int:pk>',views.CreatedScheduleDetailView, name='view_created_schedule'),
    path('<int:id>/add_schedule/', views.AddSchedule.as_view(), name='add_schedule'),
    path('<int:id>/update_schedule/<int:pk>', views.UpdateSchedule.as_view(), name='update_schedule'),
    path('<int:id>/delete_schedule/<int:pk>', views.DeleteSchedule.as_view(), name='delete_schedule'),
    path('<int:id1>/schedule/<int:id2>/bookings/', views.ViewBookings.as_view(), name='bookings'),
    
    path('<int:id>/view_schedule/<int:pk>',views.ScheduleDetailView, name='view_schedule'),
    path('<int:id1>/schedule/<int:id2>/select_seat', views.SelectSeat.as_view(), name='select_seat'),
    path('book_seat/', views.BookSeat.as_view(), name='book_seat'),
    
    path('history/', views.BookHistory.as_view(), name='book_history'),
    path('download/', views.DownloadTicket.as_view(), name='download'),
    path('ticket/<int:pk>', views.Ticket.as_view(), name ='ticket'),

    path('<int:id1>/schedule/<int:id2>/cancel_booking/<int:pk>', views.CancelBooking.as_view(), name='cancel_booking'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)