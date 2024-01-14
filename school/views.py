from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
from account.models import User
from school.models import FlashCard, FlashCardAnswerOptions
from django.contrib.auth.decorators import login_required

class FlascardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ["question", "category", "level"]
        widgets = {
            "question": forms.TextInput(attrs={'autofocus':'autofocus'}),
        }

class FlashcardOptionForm(forms.ModelForm):
    class Meta:
        model = FlashCardAnswerOptions
        fields = ["option", "right"]

AnswerOptionFormSet = forms.inlineformset_factory(
    FlashCard, FlashCardAnswerOptions, form=FlashcardOptionForm,
    extra=1, can_delete=True, can_delete_extra=True
)

def home(request):
    return render(request, 'school/home.html')



@login_required
def flashcard_list(request):

    if request.method == "POST":
        flashcard_form = FlascardForm(request.POST)
        formset = AnswerOptionFormSet(request.POST)

        print(formset)
        if flashcard_form.is_valid() and formset.is_valid():
            
            flashcard = flashcard_form.save()
            
            # Save variant formset
            answers = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for answer in answers:
                answer.question = flashcard
                answer.save()
        else:
            print(flashcard_form.errors)
            print(formset.errors)


    else:
        flashcard_form = FlascardForm()
        formset = AnswerOptionFormSet()

    flashcards = FlashCard.objects.all()
    return render(request, 'school/flashcards.html', {'flashcards':flashcards,
                                                      'flashcard_form':flashcard_form,
                                                      'formset':formset})

@login_required
def flashcard_create(request):
    pass