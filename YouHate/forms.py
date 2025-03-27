from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Video, Category
from django.core.validators import FileExtensionValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter your email in standard format.")
    picture = forms.ImageField(required=False, allow_empty_file=False, help_text="Upload a profile picture to your account. This can also be done later.")

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            uploaded_picture = self.cleaned_data.get('picture')
            if uploaded_picture:
                profile.profile_picture = uploaded_picture
            profile.save()
        return user
    
class VideoUploadForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, help_text="Choose a category.", widget=forms.Select(attrs={'class': 'category-select'}))
    title = forms.CharField(required=True, help_text="Create a title.", widget=forms.TextInput(attrs={'class': 'title-box'}))
    description = forms.CharField(required=True, help_text="Create a description.", widget=forms.Textarea(attrs={'class': 'description-box'}))
    thumbnail = forms.ImageField(required=True, allow_empty_file=False, help_text="Upload a video thumbnail.")
    video = forms.FileField(required=True, help_text="Upload your video file.", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])

    class Meta:
        model = Video
        fields = ["category", "title", "description", "thumbnail", "video"]