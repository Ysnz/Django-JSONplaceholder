from django.contrib import admin

# Register your models here.
from .models import User, Todo, Album, Photo, Post, Comment

admin.site.register(User)
admin.site.register(Todo)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Post)
admin.site.register(Comment)
