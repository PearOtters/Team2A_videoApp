"""videoapp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from YouHate import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sort-videos/', views.sort_videos, name='sort_videos'),
    path('about/', views.about, name='about'),
    path('login/', views.sign_in_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/<str:username>/', views.user_profile, name="user_profile"),
    path('random-video/', views.random_video, name='random_video'),
    path('like-video/', views.like_video, name='like_video'),
    path('dislike-video/', views.dislike_video, name='dislike_video'),
    path('add_comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('add_reply/<int:comment_id>/<int:video_id>/', views.add_reply, name='add_reply'),
    path('search/', views.search_videos, name='search_videos'),
    path('upload/', views.upload_video, name='upload_video'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:video_slug>/', views.video_detail, name='video_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)