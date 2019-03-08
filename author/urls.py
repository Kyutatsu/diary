from django.urls import path
from . import views


app_name = 'author'
urlpatterns = [
        path(
            'registration/',
            views.user_form_registration,
            name='registration',
        ),
        path(
            'profile/',
            views.AuthorProfile.as_view(),
            name='profile',
        ),
]
