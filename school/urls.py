from django.urls import path 
from . import views

app_name = 'school'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),

]