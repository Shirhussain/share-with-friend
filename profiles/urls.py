from django.urls import path

from .views import (
    my_profile_view, 
    invitation_received_view, 
    # profile_list_view, 
    invite_profiles_list_view,
    ProfileListView,
    send_invitation,
    remove_from_friend,
    accept_invitation, 
    reject_invitation,
    # ProfileDetailView,
)

app_name = 'profiles'
urlpatterns = [
    path('me/', my_profile_view, name='myprofile'),
    path('my-invitation/', invitation_received_view, name='my-invitation'),
    # path('profile-list/', profile_list_view, name='profile-list'),
    path('', ProfileListView.as_view(), name='profile-list'),
    # path('<slug>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('to-invite/', invite_profiles_list_view, name='to-invite-profile-list'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_from_friend, name='remove-friend'),
    path('my-invitation/accept/', accept_invitation, name='accept-invitation'),
    path('my-invitation/reject/', reject_invitation, name='reject-invitation'),
]
