from django.urls import path

from .views import my_profile_view

app_name = 'profiles'
urlpatterns = [
    path('me', my_profile_view, name='myprofile'),
]
