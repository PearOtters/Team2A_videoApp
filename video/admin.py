from django.contrib import admin
from video.models import Video, Category, Comment, UserProfile, Reply

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Reply)