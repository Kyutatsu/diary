from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.IndividualView.as_view(), name='individual'),
    path('make_diary/', views.make_diary, name='make_diary'),
    path(
        'update_diary/<int:pk>/',
        views.update_diary,
        name='update_diary'
    ),
    path(
        'delete_diary/<int:pk>/',
        views.delete_diary,
        name='delete_diary'
    ),
]
