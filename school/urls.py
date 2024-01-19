from django.urls import path 
from . import views

app_name = 'school'
urlpatterns = [
   
    path('flashcards/', views.flashcard_list, name='flashcard_list'),
    path('flashcards/create/', views.flashcard_create, name='flashcard_create'),
    path('flashcards/edit/<int:flashcard_id>/', views.flashcard_edit, name='flashcard_edit'),
    path('flashcards/delete/<int:flashcard_id>/', views.flashcard_delete, name='flashcard_delete'),
    path('challenges/', views.challenges, name='challenges'),






    path('', views.home, name='home'),

]