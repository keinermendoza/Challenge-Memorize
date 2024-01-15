from itertools import chain
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from account.models import User
from school.models import FlashCard, ChoicesCard, ChoicesCardAnswerOptions
from django.contrib.auth.decorators import login_required

class ChoicesCardForm(forms.ModelForm):
    class Meta:
        model = ChoicesCard
        fields = ["question", "category", "level"]
        widgets = {
            "question": forms.TextInput(attrs={'autofocus':'autofocus'}),
        }

class ChoicesCardOptionForm(forms.ModelForm):
    class Meta:
        model = ChoicesCardAnswerOptions
        fields = ["option", "right"]

AnswerOptionFormSet = forms.inlineformset_factory(
    ChoicesCard, ChoicesCardAnswerOptions, form=ChoicesCardOptionForm,
    extra=1, can_delete=True, can_delete_extra=True
)

class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = '__all__'

def home(request):
    return render(request, 'school/home.html')


@login_required
def flashcard_list(request):
    flashcards = FlashCard.objects.filter(user=request.user).values_list("question", "created", "level")
    # TODO  resolving how to acces properties 
    choicescards = ChoicesCard.objects.filter(user=request.user).values_list("question", "created", "level", "is_multiple_choice")
    cards = list(chain(flashcards, choicescards))
    print("CARDS", cards, "FLASHCARDS", flashcards, "CHOICECARDS" ,choicescards)
    flashcard_form = FlashCardForm()
    return render(request, 'school/flashcards.html', {'cards':cards,
                                                      'flashcard_form':flashcard_form})


@login_required
def choicecard_create(request):

    if request.method == "POST":
        choicescard_form = ChoicesCardForm(request.POST)
        formset = AnswerOptionFormSet(request.POST)

        print(formset)
        if choicescard_form.is_valid() and formset.is_valid():
            
            choicescard = choicescard_form.save()
            
            # Save variant formset
            answers = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for answer in answers:
                answer.question = choicescard
                answer.save()
        else:
            print(choicescard_form.errors)
            print(formset.errors)


    else:
        choicescard_form = ChoicesCardForm()
        formset = AnswerOptionFormSet()

    choicescard = ChoicesCard.objects.all()
    return render(request, 'school/flashcards.html', {'flashcards':choicescard,
                                                      'flashcard_form':choicescard_form,
                                                      'formset':formset})

@login_required
def flashcard_create(request):
    pass