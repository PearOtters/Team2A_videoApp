import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoapp_project.settings')

import django
django.setup()
from YouHate.models import Category, Video, UserProfile, Comment, Reply
from django.core.files import File
from django.utils import timezone
from django.contrib.auth.models import User

def populate():
    ###
    ### TODO: Add more videos, users, comments, and replies ###
    ###

    user1 = add_user("user1", "user1@gmail.com", 1234)
    user2 = add_user("user2", "user2@gmail.com", 1234)
    user3 = add_user("user3", "user3@gmail.com", 1234)
    user4 = add_user("user4", "user4@gmail.com", 1234)

    userProfile1 = add_userProfile(user1, score=5)
    userProfile2 = add_userProfile(user2, score=10)
    userProfile3 = add_userProfile(user3, score=15)
    userProfile4 = add_userProfile(user4, score=20)

    categories = [
        {'name': 'Music', 'video_count': 0},
        {'name': 'Comedy', 'video_count': 0},
        {'name': 'Gaming', 'video_count': 0},
        {'name': 'Education', 'video_count': 0},
        {'name': 'Sports', 'video_count': 0},
        {'name': 'Movies', 'video_count': 0},
        {'name': 'News', 'video_count': 0},
        {'name': 'Science & Technology', 'video_count': 0},
        {'name': 'Travel', 'video_count': 0},
        {'name': 'Fashion', 'video_count': 0},
        {'name': 'Vlogs', 'video_count': 0},
        {'name': 'Pets & Animals', 'video_count': 0},
        {'name': 'Food', 'video_count': 0},
        {'name': 'Fitness', 'video_count': 0},
        {'name': 'Beauty', 'video_count': 0},
        {'name': 'DIY', 'video_count': 0},
        {'name': 'Dance', 'video_count': 0},
        {'name': 'Auto', 'video_count': 0},
        {'name': 'Politics', 'video_count': 0},
        {'name': 'Lifestyle', 'video_count': 0},
        {'name': 'Kids', 'video_count': 0},
        {'name': 'Business', 'video_count': 0},
        {'name': 'Tech', 'video_count': 0},
        {'name': 'Entertainment', 'video_count': 0},
        {'name': 'Gaming', 'video_count': 0},
        {'name': 'Science', 'video_count': 0},
        {'name': 'Art', 'video_count': 0},
        {'name': 'Culture', 'video_count': 0},
        {'name': 'History', 'video_count': 0},
        {'name': 'Documentary', 'video_count': 0},
        {'name': 'Review', 'video_count': 0},
        {'name': 'Reaction', 'video_count': 0},
        {'name': 'Unboxing', 'video_count': 0},
        {'name': 'Challenge', 'video_count': 0},
        {'name': 'Prank', 'video_count': 0},
        {'name': 'Tutorial', 'video_count': 0},
    ]

    categorie_models = []

    for category in categories:
        categorie_models.append(add_category(category['name'], category['video_count']))

    video1 = add_video(
        category=categorie_models[0],
        user=userProfile1,
        title="All The Stars Kendrick Lamar",
        video_path="static/populateMedia/videos/AllTheStars_KendrickLamar.mp4",
        thumbnail_path="static/populateMedia/thumbnails/AllTheStars_KendrickLamar.jpg",
        description="Black Panther The Album out now\n" + 
        "http://smarturl.it/BlackPantherAlbum\n\n" + 
        "http://vevo.ly/3WpVJn",
        views=55_634_574,
        likes=618_000,
        dislikes=18_000
    )

    video2 = add_video(
        category = categorie_models[31],
        user=userProfile1,
        title="Me At The Zoo",
        video_path="static/populateMedia/videos/MeAtTheZoo.mp4",
        thumbnail_path="static/populateMedia/thumbnails/MeAtTheZoo.jpg",
        description="Microplastics are accumulating in human brains at an alarming rate",
        views=351_072_792,
        likes=17_000_000,
        dislikes=0
    )

    comments = [
        {'video': video1, 'user': userProfile3, 'body': 'Amazing song!', 'likes': 100_000, 'dislikes': 10},
        {'video': video1, 'user': userProfile2, 'body': 'Great!', 'likes': 10_000, 'dislikes': 100_000},
        {'video': video1, 'user': userProfile4, 'body': 'Love the new song!', 'likes': 500_000, 'dislikes': 100},
    ]

    comment_models = []

    for comment in comments:
        comment_models.append(add_comment(video=comment['video'], user=comment['user'], 
                                          body=comment['body'], likes=comment['likes'], 
                                          dislikes=comment['dislikes']))

    replies = [
        {'comment': comment_models[0], 'user': userProfile1, 'body': 'Thanks', 'likes': 10, 'dislikes': 100},
        {'comment': comment_models[1], 'user': userProfile1, 'body': 'Boring', 'likes': 100_000_000, 'dislikes': 15},
        {'comment': comment_models[2], 'user': userProfile1, 'body': 'Thanks you', 'likes': 100_000, 'dislikes': 100},
    ]
    
    for reply in replies:
        add_reply(comment=reply['comment'], user=reply['user'], body=reply['body'], 
                  likes=reply['likes'], dislikes=reply['dislikes'])

def add_category(name, video_count=0):
    category = Category.objects.get_or_create(name=name, video_count=video_count)[0]
    category.save()
    return category

def add_video(category, user, title, video_path, thumbnail_path, description="No description", created=timezone.now(), views=0, likes=0, dislikes=0):
    video_file = open(video_path, "rb")
    thumb_file = open(thumbnail_path, "rb")

    video = Video.objects.get_or_create(category=category, user=user, 
                                        title=title, description=description, 
                                        created=created, views=views, 
                                        likes=likes, dislikes=dislikes
    )[0]
    video.video.save(os.path.basename(video_path), File(video_file))
    video.thumbnail.save(os.path.basename(thumbnail_path), File(thumb_file))

    video_file.close()
    thumb_file.close()
    video.save()
    return video

def add_userProfile(user, profile_picture="static/populateMedia/profile_images/blankProfile.png", score=0):
    image_file = open(profile_picture, "rb")

    userProfile = UserProfile.objects.get_or_create(user=user, 
                                                    score=score)[0]
    userProfile.profile_picture.save(os.path.basename(profile_picture), File(image_file))

    image_file.close()
    userProfile.save()
    return userProfile

def add_user(username, email, password):
    user = User.objects.get_or_create(username=username, email=email, password=password)[0]
    user.save()
    return user

def add_comment(video, user, body, created=timezone.now(), likes=0, dislikes=0):
    comment = Comment.objects.get_or_create(video=video, user=user, 
                                  body=body, created=created, 
                                  likes=likes, dislikes=dislikes)[0]
    comment.save()
    return comment

def add_reply(comment, user, body, created=timezone.now(), likes=0, dislikes=0):
    reply = Reply.objects.get_or_create(comment=comment, user=user, body=body,
                                created=created, likes=likes, 
                                dislikes=dislikes)[0]
    reply.save()
    return reply
    
if __name__ == '__main__':
    print("Starting YouHateApp population script...")
    populate()
    print("YouHateApp population script completed!")