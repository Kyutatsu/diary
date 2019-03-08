from django.urls import path
from . import views


app_name = 'tweetdiary'
urlpatterns = [
    path(
        'tweet_drawing/<uuid:pk>/',
        views.post_drawing,
        name='tweet_drawing'
    ),
    path('get_token/', views.get_access_token, name='get_token'),
    path('select_url/', views.select_url, name='select_url'),
]
