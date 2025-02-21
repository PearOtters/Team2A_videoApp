from django.urls import path
from video import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/upload/', views.upload, name='upload'),
    path('<slug:category_slug>/<slug:video_slug>/', views.video_detail, name='video_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)