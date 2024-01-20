from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden

from django import forms
from django.core.validators import MaxValueValidator

from django_htmx.http import retarget, reswap
from school.models import StudyCategory, FlashCard, ChoicesCard, ChoicesCardAnswerOptions\
    ,Challenge, ChallengeQuestion


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

CATEGORIES = list(StudyCategory.objects.all().values_list("id","name"))
CATEGORIES.insert(0, ('', '--------'))
LEVELS = FlashCard.Level.choices
LEVELS.insert(0, ('', '--------'))
class SearchFlashcardForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES, required=False)
    level = forms.ChoiceField(choices=LEVELS, required=False)
    question = forms.CharField(max_length=20, required=False)

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
    cards = FlashCard.objects.filter(user=request.user)
    flashcard_form = FlashCardForm()
    search_form = SearchFlashcardForm(request.GET or None)

    if search_form.is_valid():
        cd = search_form.cleaned_data

        if cd["category"]:
            cards = cards.filter(category=cd["category"])
        if cd["level"]:
            cards = cards.filter(level=cd["level"])
        if cd["question"]:
            cards = cards.filter(question__icontains=cd["question"])

    if request.htmx:
        if len(search_form.errors) == 0:
            return render(request, 'school/partials/cards/list.html', {'cards':cards,
                                                                       'searching': True})
        else:
            response = render(request, 'school/partials/forms/flashcard_search.html', {'form':search_form})
            return retarget(response, "#search-form-container")
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
@require_http_methods(["GET", "POST"])
def flashcard_edit(request, flashcard_id):
    if not request.htmx:
        return HttpResponseForbidden()

    flashcard = get_object_or_404(FlashCard, id=flashcard_id, user=request.user)
    
    

    if request.method == "POST":
        form = FlashCardForm(data=request.POST, instance=flashcard)

        if form.is_valid():
            form.save()

            flashcards = request.user.flashcards.all()
            return render(request, 'school/partials/cards/list.html', {'cards':flashcards})
        else:
            response = render(request, 'school/partials/forms/flashcard_edit.html', {'form':form,
                                                                                     'flashcard_id':flashcard_id})
            return retarget(response, '#flashcard-edit-container' )


    else:
        form = FlashCardForm(instance=flashcard)
        return render(request, 'school/partials/forms/flashcard_edit.html', {'form':form,
                                                                             'flashcard_id':flashcard_id})
    


@login_required
@require_http_methods(["DELETE"])
def flashcard_delete(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, pk=flashcard_id)

    if flashcard.user != request.user:
        return HttpResponseForbidden()
    
    flashcard.delete() 
    return HttpResponse(status=204)
    

class ChallengeForm(forms.ModelForm):
    """this form REQUIRES the request object"""
    class Meta:
        model = Challenge
        fields = ["title", "level", "number_questions"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.flashcard_num = self.request.user.flashcards.count()
        super(ChallengeForm, self).__init__(*args, **kwargs)
        
        # add validation
        self.fields['number_questions'].validators.append(MaxValueValidator(self.flashcard_num))
        # add html max attribute
        self.fields['number_questions'].widget.attrs['max'] = self.flashcard_num
                                                          


@login_required
@require_http_methods(["GET" ,"POST"])
def challenges(request):
    if request.method == "POST":
        form = ChallengeForm(data=request.POST, request=request)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.user = request.user
            challenge.save()

            question_set = request.user.flashcards.all().order_by("?")[:challenge.number_questions]
            print(dir(challenge))
            
            challenge.questions.add(*question_set)

            return redirect(reverse('school:start_challenge', args=[challenge.id]))
        
    form = ChallengeForm(request=request)
    return render(request, 'school/challenges.html', {'challenge_form':form})

def start_challenge(request, challenge_id):
    return render(request, 'school/challenges/detail.html')


def challenge_resume(request, challenge_id):
    return render(request, 'school/challenges/resume.html')

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

