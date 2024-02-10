from django.urls import path 
from . import views
from . import challenge_views

app_name = 'school'
urlpatterns = [
   
    path('flashcards/', views.flashcard_list, name='flashcard_list'),
    path('flashcards/create/', views.flashcard_create, name='flashcard_create'),
    path('flashcards/create/fresh-form/', views.fresh_flashcard_form, name='fresh_flashcard_form'),

    path('flashcards/edit/<int:flashcard_id>/', views.flashcard_edit, name='flashcard_edit'),
    path('flashcards/delete/<int:flashcard_id>/', views.flashcard_delete, name='flashcard_delete'),
    path('flashcards/category/create/', views.category_create, name='category_create'),



    path('challenges/', challenge_views.challenges, name='challenges'),
    path('challenge/filter/', challenge_views.challenge_filter, name='challenge_filter'),
    path('challenge/create/', challenge_views.challenge_create, name='challenge_create'),


    path('challenge/start/<int:challenge_id>', challenge_views.start_challenge, name='start_challenge'),
    path('challenge/answer/<int:question_id>/', challenge_views.challenge_answer, name='challenge_answer'),

    path('challenge/resume/<int:challenge_id>', challenge_views.challenge_resume, name='challenge_resume'),
    path('challenge/update/<int:challenge_id>', challenge_views.challenge_resume, name='challenge_resume'),
    path('challenge/update-form/', challenge_views.update_sections_challenge_form, name='update_sections_challenge_form'),




    path('', views.home, name='home'),

]