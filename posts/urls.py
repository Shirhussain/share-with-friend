from django.urls import  path
from .views import post_comment_create_list_view, like_unlike_post

app_name = 'posts'
urlpatterns = [
    path('', post_comment_create_list_view, name='post_comment_list'),
    path('reaction', like_unlike_post, name='reaction'),
]
