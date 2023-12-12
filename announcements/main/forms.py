from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from .models import Announcement

class RegistrationForm(UserCreationForm):
    location = forms.CharField(max_length=255, required=False, help_text='Optional.')

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'location')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # Set help_text for password1 field to an empty string
        self.fields['password1'].help_text = ''


class LoginForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['subject', 'title', 'content', 'access']

class UpdateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'access']

class AnnouncementAdminForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'location')