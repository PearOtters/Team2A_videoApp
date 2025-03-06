from django.shortcuts import render, redirect
from django.http import HttpResponse
from YouHate.models import Video, Category, Comment, UserProfile, Reply
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    context_dict = {}
    try:
        context_dict['categories'] = Category.objects.values_list('name', flat=True).order_by('-video_count')[:5]
        context_dict['videos'] = Video.objects.all()
    except Category.DoesNotExist:
        context_dict['categories'] = None
        context_dict['videos'] = None
    return render(request, 'YouHate/index.html', context=context_dict)

def about(request):
    return HttpResponse("Under construction...")

### Unused view ###
def view_categories(request):
    context_dict = {}
    context_dict['categories'] = Category.objects.order_by('-video_count')
    return render(request, 'YouHate/categories.html', context=context_dict)

def category_detail(request, category_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_slug)
        videos = Video.objects.filter(category=category)
        context_dict['videos'] = videos
        context_dict['videosViews'] = videos.order_by('-views')
        context_dict['videosLikes'] = videos.order_by('-likes')
        context_dict['videosCreated'] = videos.order_by('-created')
        context_dict['videosDislikes'] = videos.order_by('-dislikes')
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['videos'] = None
    return render(request, 'YouHate/category_detail.html', context=context_dict)

def video_detail(request, category_slug, video_slug):
    return HttpResponse("Under construction...")

def user_login(request):
    return HttpResponse("Under construction...")

def register(request):
    return HttpResponse("Under construction...")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def upload(request, category_slug):
    return HttpResponse("Under construction...")

### Unused view ###
@login_required
def add_category(request):
    return HttpResponse("Under construction...")