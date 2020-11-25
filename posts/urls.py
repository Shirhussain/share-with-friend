from django.urls import  path
from .views import post_comment_create_list_view, like_unlike_post, PostUpdateView, PostDeleteView

app_name = 'posts'
urlpatterns = [
    path('', post_comment_create_list_view, name='post_comment_list'),
    path('reaction/', like_unlike_post, name='reaction'),
    path('update/<pk>/', PostUpdateView.as_view(), name='post-update'),
    path('delete/<pk>/', PostDeleteView.as_view(), name='post-delete'),
]
