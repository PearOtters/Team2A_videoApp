from django.shortcuts import render, redirect
from django.http import HttpResponse
from video.models import Video, Category, Comment, UserProfile, Reply
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'video/index.html')

def about(request):
    return HttpResponse("Under construction...")

def view_categories(request):
    context_dict = {}
    context_dict['categories'] = Category.objects.order_by('-video_count')
    return render(request, 'video/categories.html', context=context_dict)

def category_detail(request):
    return HttpResponse("Under construction...")

def video_detail(request):
    return HttpResponse("Under construction...")

def user_login(request):
    return HttpResponse("Under construction...")

def register(request):
    return HttpResponse("Under construction...")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('video:index'))

@login_required
def upload(request):
    return HttpResponse("Under construction...")

@login_required
def add_category(request):
    return HttpResponse("Under construction...")