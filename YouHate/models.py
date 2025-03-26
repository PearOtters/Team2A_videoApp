from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import secrets, string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default="/profile_pictures/blankProfile.png")
    bio = models.TextField(default="This user has no bio.")
    score = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    video_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Video(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])]
    )
    thumbnail = models.ImageField(upload_to='thumbnails/')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    disliked_by = models.ManyToManyField(UserProfile, related_name='disliked_videos', blank=True, default=None)
    liked_by = models.ManyToManyField(UserProfile, related_name='liked_videos', blank=True, default=None)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.category.video_count += 1
            self.category.save()
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            random_slug = ''.join(secrets.choice(alphabet) for i in range(16))
            if not Video.objects.filter(slug=random_slug).exists():
                return random_slug
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.id
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.id