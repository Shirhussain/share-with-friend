from django.contrib import admin
from .models import Post, Comment, Like 

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
