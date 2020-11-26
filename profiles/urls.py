from django.urls import path

from .views import (
    my_profile_view, 
    invitation_received_view, 
    profile_list_view, 
    invite_profiles_list_view
)

app_name = 'profiles'
urlpatterns = [
    path('me/', my_profile_view, name='myprofile'),
    path('my-invitation/', invitation_received_view, name='my-invitation'),
    path('profile-list/', profile_list_view, name='profile-list'),
    path('to-invite/', invite_profiles_list_view, name='to-invite-profile-list'),
]
