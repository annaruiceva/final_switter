from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm)
from django.utils.translation import gettext_lazy as _

from main_twitter.models import Profile, Comment

User = get_user_model()


class CreatePostForm(forms.Form):
    text = forms.CharField()


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UpdateProfileForm(forms.ModelForm):
    # avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    status = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    # image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['about', 'status', 'image']


class CreateCommentForm(forms.ModelForm):
    text = forms.CharField()

    class Meta:
        model = Comment
        fields = ['text',]
