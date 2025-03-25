from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from YouHate.models import Video, Category, Comment, UserProfile, Reply
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError
from .forms import CustomUserCreationForm
import random, json

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
    return base(request, 'YouHate/about.html', {})

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
        currentUser = None
        if request.user.is_authenticated:
            currentUser = request.user
            try:
                currentUserProfile = UserProfile.objects.get(user=currentUser)
                if currentUserProfile in thisVideo.liked_by.all():
                    context_dict['liked'] = True
                if currentUserProfile in thisVideo.disliked_by.all():
                    context_dict['disliked'] = True
            except UserProfile.DoesNotExist:
                currentUserProfile = None

        thisVideo.views += 1
        thisVideo.save()

        suggested = videos.order_by('-dislikes')
        ratio = 0
        if thisVideo.likes > 0:
            ratio = (thisVideo.dislikes / thisVideo.likes) * 100
        elif thisVideo.dislikes > 0:
            ratio = 100

        context_dict['currentUser'] = currentUser
        context_dict['ratio'] = ratio
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
        categories = Category.objects.values_list('slug', 'name').order_by('name')
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
    return base(request, "YouHate/register.html", context_dic)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

def user_profile(request, username):
    context_dict = {}
    user_profile = UserProfile.objects.get(user__username=username)
    videos = Video.objects.filter(user=user_profile).order_by('created')
    categories = Category.objects.values_list('name', flat=True)
    top5 = Category.objects.values_list('slug', 'name').order_by('-video_count')[:5]
    context_dict['user_profile'] = user_profile
    context_dict['videos'] = videos
    context_dict['baseCategoryNames'] = categories
    context_dict['baseTop5Categories'] = top5

    return base(request, 'YouHate/profile.html', context_dict)

@login_required
def upload(request, category_slug):
    return HttpResponse("Under construction...")

def random_video(request):
    try:
        videos = Video.objects.all()
        if videos.exists():
            random_video = random.choice(videos)
            return redirect('video_detail', 
                           category_slug=random_video.category.slug,
                           video_slug=random_video.slug)
        else:
            return redirect('index')
    except Exception:
        return redirect('index')
    
@login_required
def like_video(request):
    return likeDislikeHelper(request, 1)

@login_required
def dislike_video(request):
    return likeDislikeHelper(request, -1)

def likeDislikeHelper(request, add):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_id = data.get('video_id')
        user_id = data.get('user_id')
        
        try:
            hasLiked = False
            hasDisliked = False
            video = Video.objects.get(id=video_id)
            user = UserProfile.objects.get(user_id=user_id)
            if (user != None):
                if (add < 0):
                    if user in video.disliked_by.all():
                        video.disliked_by.remove(user)
                        video.dislikes -= 1
                    else:
                        video.disliked_by.add(user)
                        video.dislikes += 1
                        hasDisliked = True
                        if user in video.liked_by.all():
                            video.liked_by.remove(user)
                            video.likes -= 1
                elif (add > 0):
                    if user in video.liked_by.all():
                        video.liked_by.remove(user)
                        video.likes -= 1
                    else:
                        video.liked_by.add(user)
                        video.likes += 1
                        hasLiked = True
                        if user in video.disliked_by.all():
                            video.disliked_by.remove(user)
                            video.dislikes -= 1
            else:
                return JsonResponse({'success': False, 'error': 'User not logged in'}, status=404)
            
            video.save()
            ratio = 0
            if video.likes > 0:
                ratio = (video.dislikes / video.likes) * 100
            elif video.dislikes > 0:
                ratio = 100
            
            return JsonResponse({
                'success': True,
                'dislikes': video.dislikes,
                'hasLiked': hasLiked,
                'hasDisliked': hasDisliked,
                'ratio': ratio
            })
        except Video.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Video not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=video_id)
            user_profile = UserProfile.objects.get(user=request.user)
            body = request.POST.get('body', '').strip()
            
            if body:
                comment = Comment(video=video, user=user_profile, body=body)
                comment.save()
                messages.success(request, 'Comment added successfully!')
            else:
                messages.error(request, 'Comment cannot be empty.')
            
            return redirect('video_detail', 
                            category_slug=video.category.slug, 
                            video_slug=video.slug)
        
        except Video.DoesNotExist:
            messages.error(request, 'Video not found.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('index')
    
    return redirect('index')

@login_required
def add_reply(request, comment_id, video_id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=video_id)
            comment = Comment.objects.get(id=comment_id)
            user_profile = UserProfile.objects.get(user=request.user)
            body = request.POST.get('body', '').strip()
            
            if body:
                reply = Reply(user=user_profile, body=body, comment=comment)
                reply.save()
                messages.success(request, 'Reply added successfully!')
            else:
                messages.error(request, 'Reply cannot be empty.')
            
            return redirect('video_detail', 
                            category_slug=video.category.slug, 
                            video_slug=video.slug)
        
        except Video.DoesNotExist:
            messages.error(request, 'Video not found.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('index')
    
    return redirect('index')

def search_videos(request):
    query = request.GET.get('query', '')
    filter_type = request.GET.get('filter', 'video')
    context_dict = {}

    try:
        if filter_type == 'creator':
            videos = Video.objects.filter(user__user__username__icontains=query)
        elif filter_type == 'category':
            videos = Video.objects.filter(category__name__icontains=query)
        else:
            videos = Video.objects.filter(title__icontains=query)

        context_dict['videos'] = videos
        context_dict['query'] = query
        context_dict['filter_type'] = filter_type
    except Exception as e:
        context_dict['videos'] = None
        context_dict['error'] = str(e)

    return base(request, 'YouHate/search_results.html', context_dict)

def sign_in_view(request):
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                print(username)
                password = login_form.cleaned_data['password']
                print(password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    login_form.add_error(None, 'Invalid username or password')

    return base(request, 'YouHate/sign_in.html', {'login_form': login_form})