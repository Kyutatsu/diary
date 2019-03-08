from django.urls import path
from . import views


app_name = 'board'
urlpatterns = [
        path('', views.BoardListView.as_view(), name='board_list'),
        path(
            'board/<uuid:pk>/',
            views.TopicListView.as_view(),
            name='topic_list'
        ),
        path(
            'topic/<uuid:pk>/',
            views.TopicIndividualView.as_view(),
            name='topic'
        ),
        path(
            'topic/makepost/<uuid:pk>/',
            views.make_post,
            name='make_post'
        ),
        path(
            'topic/maketopic/<uuid:pk>/',
            views.TopicCreate.as_view(),
            name='make_topic'
        ),
]
