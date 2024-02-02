import json
from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden, QueryDict
from django.db.models import Count, F, Case, When, Q

from django import forms

from django_htmx.http import retarget, reswap, trigger_client_event
from school.models import (
    StudyCategory,
    FlashCard,
    Challenge,
    ChallengeQuestion,
)

from .forms import FilterChallengeForm, FlashCardForm, ChallengeForm, category_field_partial, SearchFlashcardForm



def home(request):
    return render(request, "school/home.html")


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
            return render(
                request,
                "school/partials/cards/list.html",
                {"cards": cards, "searching": True},
            )
        else:
            response = render(
                request,
                "school/partials/forms/flashcard_search.html",
                {"form": search_form},
            )
            response = retarget(response, "#search-form-container")
            return trigger_client_event(response, 'clean_errors')
        
    return render(
        request,
        "school/flashcards.html",
        {"cards": cards, "flashcard_form": flashcard_form, "search_form": search_form},
    )



@login_required
@require_http_methods(["GET", "POST"])
def challenges(request):
    
    challenges = request.user.challenges.all()
    challenge_form = ChallengeForm(request=request)
    filter_challenge_form = FilterChallengeForm(data=request.GET or None)

    if filter_challenge_form.is_valid():
        cd = filter_challenge_form.cleaned_data
        
        if cd["status"]:
            challenges = challenges.filter(status=cd["status"])
        if cd["level"]:
            challenges = challenges.filter(level=cd["level"])
        if cd["category"]:
            challenges = challenges.filter(questions__category=cd["category"]).distinct()

    # returning partials in when using htmx
    if request.htmx:
        
        if len(filter_challenge_form.errors) == 0:
            response = render(
                request,
                "school/partials/challenges/table.html",
                {"challenges": challenges},
            )
            return trigger_client_event(response, 'clean_errors')
        else:
            response = render(
                request,
                "school/partials/forms/challenge_filter.html",
                {"filter_challenge_form": filter_challenge_form},
            )
            return retarget(response, "#challenges-filter-form-container")


    if request.method == "POST":
        challenge_form = ChallengeForm(data=request.POST, request=request)
        
        if challenge_form.is_valid():

            cd = challenge_form.cleaned_data
            flashcards_in_categories = request.user.flashcards.filter(category__in=cd['category']).count()

            if not flashcards_in_categories:
                challenge_form.add_error(None, "You don't have a flashcard in the selected categories")
            else:   
                challenge = challenge_form.save(commit=False)
                challenge.user = request.user
                challenge.save()

                question_set = request.user.flashcards.filter(category__in=cd['category']).order_by("?")[
                    : challenge.number_questions
                ]

                challenge.questions.add(*question_set)

                return redirect(reverse("school:start_challenge", args=[challenge.id]))
        else:
            print(challenge_form.errors)   
    return render(request, "school/challenges.html", {"challenge_form": challenge_form,
                                                      "filter_challenge_form": filter_challenge_form,
                                                      'challenges':challenges,})






@login_required
@require_http_methods(["GET"])
def update_sections_challenge_form(request):
    level = request.GET.get('level', None)
    if level:
        form = category_field_partial(level=level)
        return render(request, 'school/partials/forms/challenge_create_sections/category.html', {'form':form})
    print(request.GET)
    category = request.GET.get('category', None)
    if category:
        form =  category_field_partial(level=level, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
        else:
            print(form.errors)
    return HttpResponse(status=204)

@login_required
@require_http_methods(["POST"])
def flashcard_create(request):
    form = FlashCardForm(request.POST)

    if form.is_valid():
        flashcard = form.save(commit=False)
        flashcard.user = request.user
        flashcard.save()

        # cards = get_all_user_cards(request)
        return render(
            request,
            "school/partials/cards/detail.html",
            {"card": flashcard, "new_card": True},
        )
    else:
        response = render(
            request,
            "school/partials/forms/create_flashcard.html",
            {"flashcard_form": form},
        )
        response = reswap(response, "innerHTML")
        return retarget(response, "#flashcard-form-container")


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
            response = render(
                request, "school/partials/cards/list.html", {"cards": flashcards}
            )
            return trigger_client_event(response, 'clean_errors')
        
        else:
            response = render(
                request,
                "school/partials/forms/flashcard_edit.html",
                {"form": form, "flashcard_id": flashcard_id},
            )
            return retarget(response, "#flashcard-edit-container")

    else:
        form = FlashCardForm(instance=flashcard)
        return render(
            request,
            "school/partials/forms/flashcard_edit.html",
            {"form": form, "flashcard_id": flashcard_id},
        )


@login_required
@require_http_methods(["DELETE"])
def flashcard_delete(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, pk=flashcard_id)

    if flashcard.user != request.user:
        return HttpResponseForbidden()

    flashcard.delete()
    return HttpResponse(status=204)





def start_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    questions = []
    for question in challenge.challenge_questions.all():
        questions.append(
            {
                "id": question.id,  # intermediate model
                "question": question.flashcard.question,
                "answer": question.flashcard.answer,
                "level": question.flashcard.get_level_display(),
                "category": question.flashcard.category.name,
                "answered": question.answered,  # intermediate model
                "correct": question.correct_answered,  # intermediate model
                "url": question.get_response_url(),  # intermediate model
            }
        )

    return render(
        request,
        "school/challenges/detail.html",
        {"questions": questions, "challenge_id": challenge_id},
    )


@require_http_methods("PUT")
def challenge_answer(request, question_id):
    question = get_object_or_404(ChallengeQuestion, pk=question_id)
    try:
        data = json.loads(request.body)


        user_response = data.get("correct")
        if user_response is not None:
            question.answered = True
            question.correct_answered = user_response
            question.save()


            ## here check for update challenge status
            remainds = question.challenge.challenge_questions.aggregate(count=Count("id", filter=Q(answered=False))) 
            if remainds.get('count') == 0:
                question.challenge.status = Challenge.Status.COMPLETE
                question.challenge.save()

            return HttpResponse(status=204)
    except:
        pass
    return HttpResponse(status=400)


def challenge_resume(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    results_by_category = list(
        challenge.challenge_questions.values(
            category=F("flashcard__category__name")
        ).annotate(
            answered=Count(Case(When(answered=True, then=1))),
            correct=Count(Case(When(correct_answered=True, then=1))),
        )
    )

    general_results = challenge.challenge_questions.aggregate(
        answered=Count("id", filter=Q(answered=True)),
        correct=Count("id", filter=Q(correct_answered=True)),
        wrong=Count("id", filter=Q(correct_answered=False)),
    )

    data = {
        'detail': results_by_category,
        'general': general_results
    }

    return render(request, "school/challenges/resume.html", {'data':data})


