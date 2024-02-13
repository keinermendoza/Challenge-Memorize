from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from account.models import User

from account.forms import RegisterForm, LoginForm

@require_http_methods(["GET", "POST"])
def register(request):
    """
        GET: render Registration Page with RegisterForm
        POST: validate the RegisterForm, returns:
            - validation success: home page '/'
            - validation fail: render the same page showing error's form   
    """
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(email=cd["email"],
                                     password=cd["password"],
                                     username=cd["name"])
            login(request, user)
            return redirect(reverse("school:flashcard_list"))
        
    return render(request, "school/register.html", {"form":form})             

def login_view(request):
    """
        GET: catch page requested by user if exist and render Login Page with LoginForm
        POST: validate the LoginForm, returns:
            - validation success: redirects to:
                - previous page requested by user if page exists
                - home page '/' by default

            - validation fail: render the same page showing error's form   
    """
    form = LoginForm()
    next_page = request.GET.get("next", None)
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd["email"], password=cd["password"])
            
            if user is not None:
                login(request, user)
                
                # Check previous page requested before redirect
                if page_requested := cd.get("next", None):
                    resolver_page = resolve(page_requested)
                    if resolver_page.url_name:                    
                        return redirect(page_requested)

                return redirect(reverse("school:home"))
            else:
                form.add_error(None, "Sorry, Invalid Email or Password")    
    return render(request, "school/login.html", {"form":form, "next":next_page})

def logout_view(request):
    logout(request)
    return redirect(reverse("account:login"))