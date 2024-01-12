from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from account.models import User
from django.contrib.auth import login, logout, authenticate


class RegisterForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
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
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

def home(request):
    return render(request, 'school/home.html')

def register(request):
    if request.method not in ["GET", "POST"]:
        return HttpResponseNotAllowed(permitted_methods=["POST", "GET"])
    
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(email=cd["email"],
                                     password=cd["password"],
                                     username=cd["name"])
            
            return HttpResponse(f"""rgistred user {user.username},
                                with the email {user.email},
                                and hash password {user.password}""")
        
    return render(request, "school/register.html", {"form":form})             

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.clean_data
            user = authenticate(email=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect(reverse("school:home"))
    return render(request, "school/login.html", {"form":form})

def logout_view(request):
    logout(request)
    return redirect(reverse("school:login"))