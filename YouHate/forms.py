from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Video

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
    class Meta:
        model = Video
        fields = ["category", "title", "description", "thumbnail", "video"]
