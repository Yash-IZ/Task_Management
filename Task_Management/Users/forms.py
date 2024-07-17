# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'name', 'designation', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)  

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']