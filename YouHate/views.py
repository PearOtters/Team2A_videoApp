from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from YouHate.models import Video, Category, Comment, UserProfile, Reply
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError
from .forms import CustomUserCreationForm

def index(request):
    context_dict = {}
    try:
        context_dict['categories'] = Category.objects.order_by('-video_count')[:5]
        context_dict['videos'] = Video.objects.all()
        context_dict['recentVideos'] = Video.objects.order_by('created')[:10]
    except Category.DoesNotExist:
        context_dict['categories'] = None
        context_dict['videos'] = None
        context_dict['recentVideos'] = None
    return base(request, 'YouHate/index.html', context_dict)

def about(request):
    return render(request, 'YouHate/about.html')

def category_detail(request, category_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_slug)
        videos = Video.objects.filter(category=category)
        context_dict['videos'] = videos
        context_dict['recentVideos'] = videos.order_by('created')
        context_dict['dislikedVideos'] = videos.order_by('-dislikes')
        context_dict['mostViewedVideos'] = videos.order_by('-views')
        context_dict['leastViewedVideos'] = videos.order_by('views')
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['videos'] = None
    return base(request, 'YouHate/category_detail.html', context_dict)

def video_detail(request, category_slug, video_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_slug)
        videos = Video.objects.filter(category=category)
        thisVideo = videos.filter(slug=video_slug)[0]
        suggested = videos.order_by('-dislikes')

        context_dict['comments'] = Comment.objects.filter(video=thisVideo)
        context_dict['replies'] = Reply.objects.all()
        context_dict['thisVideo'] = thisVideo
        context_dict['suggestedVideo'] = suggested[0] # if not (suggested[0] in suggested.filter(slug=video_slug)) else suggested[1]

    except Video.DoesNotExist:
        context_dict['comments'] = None
        context_dict['replies'] = None
        context_dict['thisVideo'] = None
        context_dict['suggestedVideo'] = None
    return base(request, "YouHate/video_detail.html", context_dict)

def base(request, url, context_dic):
    try:
        categories = Category.objects.values_list('name', flat=True)
        top5 = Category.objects.values_list('slug', 'name').order_by('-video_count')[:5]
        context_dic['baseCategoryNames'] = categories
        context_dic['baseTop5Categories'] = top5
    except Category.DoesNotExist:
        context_dic['baseCategoryNames'] = None
    return render(request, url, context=context_dic)

def sort_videos(request):
    category_slug = request.GET.get("category")
    sort_by = request.GET.get("sort", "-created")

    if not category_slug:
        return JsonResponse({"error": "No category provided"}, status=400)

    category = get_object_or_404(Category, slug=category_slug)
    videos = Video.objects.filter(category=category).order_by(sort_by)

    video_list = [{
            "title": v.title,
            "thumbnail": v.thumbnail.url,
            "category_slug": v.category.slug,
            "slug": v.slug,
            "username": v.user.user.username,
            "created": v.created.strftime("%d.%m.%Y"),
            "dislikes": v.dislikes,
            "views": v.views,
        } for v in videos]
    
    return JsonResponse({"videos": video_list})

def user_login(request):
    return redirect("register")

def user_register(request):
    if request.method == "POST":
        registerForm = CustomUserCreationForm(request.POST, request.FILES)
        if registerForm.is_valid():
            registerForm.save()
            return redirect("index")
    else:
        registerForm = CustomUserCreationForm()
    context_dic = {"form": registerForm}
    return render(request, "YouHate/register.html", context=context_dic)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def user_profile(request, username):
    context_dict = {}
    user_profile = UserProfile.objects.get(user__username=username)
    videos = Video.objects.filter(user=user_profile).order_by('-created')
    categories = Category.objects.values_list('name', flat=True)
    top5 = Category.objects.values_list('slug', 'name').order_by('-video_count')[:5]
    context_dict['user_profile'] = user_profile
    context_dict['videos'] = videos
    context_dict['baseCategoryNames'] = categories
    context_dict['baseTop5Categories'] = top5

    return render(request, 'YouHate/profile.html', context_dict)

@login_required
def upload(request, category_slug):
    return HttpResponse("Under construction...")