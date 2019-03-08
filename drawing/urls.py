from django.urls import path
from . import views

app_name = 'drawing'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('drawing/', views.DrawingView.as_view(), name='drawing'),
        path(
            '<uuid:pk>/',
            views.IndividualView.as_view(),
            name='individual'
        ),
        path('delete/<uuid:pk>', views.delete, name='delete'),

]
