from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'querys'
urlpatterns=[
    path('<int:id>/discussions/',views.viewDiscussions,name='discussions'),
    path('<int:id>/add/',views.AddQuery.as_view(), name='add'),
    path('<int:id>/myqueries/',views.ListQueries.as_view(), name='myqueries'),
    path('<int:id>/update/<int:pk>',views.UpdateQuery.as_view(), name='update'),
    path('<int:id>/delete/<int:pk>',views.DeleteQuery.as_view(), name='delete'),
    path('<int:id>/detail/<int:pk>',views.QueryDetailView, name='query-detail'),

    path('<int:id>/query/<int:pk>/answer/',views.QueryAnswer, name='queryAnswer'),

    path('<int:id>/search_querys', views.search_queries, name='search_queries'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
