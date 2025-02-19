from django.shortcuts import render, redirect
from django.http import HttpResponse
from video.models import Video, Category, Comment, UserProfile, Reply
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime 

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

def login_view(request):
    return HttpResponse("Under construction...")

def logout_view(request):
    return HttpResponse("Under construction...")

def register(request):
    return HttpResponse("Under construction...")

def upload(request):
    return HttpResponse("Under construction...")

def add_category(request):
    return HttpResponse("Under construction...")