from django.urls import path 
from . import views

app_name = 'school'
urlpatterns = [
   
    path('flashcards/', views.flashcard_list, name='flashcard_list'),
    path('flashcards/create/', views.flashcard_create, name='flashcard_create'),
    path('flashcards/edit/<int:flashcard_id>/', views.flashcard_edit, name='flashcard_edit'),
    path('flashcards/delete/<int:flashcard_id>/', views.flashcard_delete, name='flashcard_delete'),
    path('challenges/', views.challenges, name='challenges'),
    path('challenge/start/<int:challenge_id>', views.start_challenge, name='start_challenge'),
    path('challenge/answer/<int:question_id>/', views.challenge_answer, name='challenge_answer'),

    path('challenge/resume/<int:challenge_id>', views.challenge_resume, name='challenge_resume'),
    path('challenge/update/<int:challenge_id>', views.challenge_resume, name='challenge_resume'),
    path('challenge/update-form/', views.update_sections_challenge_form, name='update_sections_challenge_form'),




    path('', views.home, name='home'),

]