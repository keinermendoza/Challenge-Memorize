from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseNotAllowed
from account.models import User

from account.forms import RegisterForm, LoginForm

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