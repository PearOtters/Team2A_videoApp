from django.urls import path
from video import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('categories/', views.view_categories, name='view_categories'),
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/<slug:video_slug>/', views.video_detail, name='video_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('categories/<slug:category_slug>/upload/', views.upload, name='upload'),
    path('categories/add_category/', views.add_category, name='add_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)