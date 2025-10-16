from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']  # change these fields to match your Profile model

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 != pw2:
            raise forms.ValidationError("Passwords do not match.")
        return pw2

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")

class UsernameResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Enter your username")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist. You can create a new account.")
        return username
