from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden
from django import forms
from django_htmx.http import retarget, reswap
from school.models import StudyCategory, FlashCard, ChoicesCard, ChoicesCardAnswerOptions

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
        exclude = ["user"]


# utils
def get_all_user_cards(request):
    flashcards = FlashCard.objects.filter(user=request.user)
    choicescards = ChoicesCard.objects.filter(user=request.user)
        
    cards = list(chain(flashcards, choicescards))
    sorted_cards = sorted(cards, key=attrgetter("created"), reverse=True)
    return sorted_cards


def home(request):
    return render(request, 'school/home.html')


@login_required
def flashcard_list(request):
    cards = get_all_user_cards(request)
    flashcard_form = FlashCardForm()
    search_form = SearchForm()
    print(search_form)
    return render(request, 'school/flashcards.html', {'cards':cards,
                                                      'flashcard_form':flashcard_form,
                                                      'search_form': search_form})

# @login_required
# def flashcard_search(request):
#     # cards = get_all_user_cards(request)
#     flashcards = FlashCard.objects.filter(user=request.user)

#     return render(request, 'school/flashcards.html', {'cards':cards,
#                                                       'flashcard_form':flashcard_form})


@login_required
@require_http_methods(["POST"])
def flashcard_create(request):
    form = FlashCardForm(request.POST)
    
    if form.is_valid():
        flashcard = form.save(commit=False)
        flashcard.user = request.user
        flashcard.save()

        # cards = get_all_user_cards(request)
        return render(request, 'school/partials/cards/detail.html', {'card':flashcard,
                                                                    'new_card':True})
    else:
        response =  render(request, 'school/partials/forms/create_flashcard.html', {'flashcard_form':form})
        response = reswap(response, "innerHTML")
        return retarget(response, '#flashcard-form-container')
    
@login_required
@require_http_methods(["DELETE"])
def flashcard_delete(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, pk=flashcard_id)

    if flashcard.user != request.user:
        return HttpResponseForbidden()
    
    flashcard.delete() 
    return HttpResponse(status=204)
    



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

