from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus":"autofocus"}))
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        cd = super().clean()
        if cd.get("password") != cd.get("confirm_password"):
            raise forms.ValidationError("passwords dosen't match")
        return cd 
    
    def clean_name(self):
        cd = super().clean()
        name = cd.get("name")
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("this name is allready taken")
        return name
    
    def clean_email(self):
        cd = super().clean()
        email = cd.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("this email is allready taken")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus":"autofocus"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    next = forms.CharField(required=False)