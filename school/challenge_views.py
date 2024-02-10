import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Count, F, Case, When, Q

from django_htmx.http import retarget, reswap, trigger_client_event, HttpResponseClientRedirect
from school.models import (
    Challenge,
    ChallengeQuestion,
)

from .forms import (
    FilterChallengeForm,
    ChallengeForm,
    category_field_partial,
)

@login_required
@require_http_methods(["GET", "POST"])
def challenges(request):
    """
        GET: display list of user's challenges
            creation challenge form
            filter challenge form
    """

    challenges = request.user.challenges.all()
    challenge_form = ChallengeForm(request=request)
    filter_challenge_form = FilterChallengeForm()

        

    return render(
        request,
        "school/challenges.html",
        {
            "challenge_form": challenge_form,
            "filter_challenge_form": filter_challenge_form,
            "challenges": challenges,
        },
    )

@login_required
@require_http_methods(["POST"])
def challenge_create(request):
    """
        HX-POST: handles the creation of new challenge using ChallengeForm
            returns:
            - validation success: redirection to school:start_challenge
            - validation error: the same view when GET but with ChallengeForm errors
    """
    if not request.htmx:
        return HttpResponseForbidden()
    
    form = ChallengeForm(data=request.POST, request=request)

    if form.is_valid():
        cd = form.cleaned_data

        challenge = form.save(commit=False)
        challenge.user = request.user
        challenge.save()
        form.save_m2m()

        question_set = request.user.flashcards.filter(
            category__in=cd["categories"]
        ).filter(level=cd["level"]).order_by("?")[: challenge.number_questions]

        challenge.questions.add(*question_set)
        return HttpResponseClientRedirect(reverse("school:start_challenge", args=[challenge.id]))
    
    response = render(
            request,
            "school/partials/forms/challenge_create.html",
            {"form": form},
        )
    response = retarget(response, "#challenge-form-container")
    return reswap(response, 'innerHTML')

@login_required
@require_http_methods(["GET"])
def challenge_filter(request):
    """
      HX-GET: handles the filtration list of user's challenges using FilterChallengeForm
            returns parital of: 
            - validation success: new list of challenges
            - validation error: filter form with errors
    """
    if not request.htmx:
        return HttpResponseForbidden()
    
    challenges = request.user.challenges.all()
    filter_challenge_form = FilterChallengeForm(request.GET)

     # FILTERING challenges list
    if filter_challenge_form.is_valid():
        cd = filter_challenge_form.cleaned_data

        if cd["status"]:
            challenges = challenges.filter(status=cd["status"])
        if cd["level"]:
            challenges = challenges.filter(level=cd["level"])
        if cd["category"]:
            challenges = challenges.filter(categories=cd["category"])

        # if len(filter_challenge_form.errors) == 0:

        response = render(
            request,
            "school/partials/challenges/table.html",
            {"challenges": challenges},
        )
        return trigger_client_event(response, "clean_errors")
    else:
        response = render(
            request,
            "school/partials/forms/challenge_filter.html",
            {"filter_challenge_form": filter_challenge_form},
        )
        return retarget(response, "#challenges-filter-form-container")
    


@login_required
@require_http_methods(["GET"])
def update_sections_challenge_form(request):
    """
        updates the categories section in the ChallengeForm
        returns:
            - validation success: a section-form partial with categories from FlashCard related to certain level
            - validation fails: HTTP HEADER with status 400
    """
    if request.htmx:
        level = request.GET.get("level", None)
        if level:
            form = category_field_partial(level=level)
            return render(
                request,
                "school/partials/forms/challenge_create_sections/category.html",
                {"form": form},
            )
    return HttpResponse(status=400)

@require_http_methods(["GET"])
def start_challenge(request, challenge_id):
    """
        displays template with a json script of all questions challenge data 
    """
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
    """
        updates state of ChallengeQuestion
        changes the value of challenge.status when all questions be answered
        returns:
            HTTP HEADER with satatus 204 or 400
    """
    question = get_object_or_404(ChallengeQuestion, pk=question_id)
    try:
        data = json.loads(request.body)

        user_response = data.get("correct")
        if user_response is not None:
            question.answered = True
            question.correct_answered = user_response
            question.save()

            ## here check for update challenge status
            remainds = question.challenge.challenge_questions.aggregate(
                count=Count("id", filter=Q(answered=False))
            )
            if remainds.get("count") == 0:
                question.challenge.status = Challenge.Status.COMPLETE
                question.challenge.save()

            return HttpResponse(status=204)
    except:
        pass
    return HttpResponse(status=400)

@require_http_methods("GET")
def challenge_resume(request, challenge_id):
    """
        displays template with a json script of all challenge data 
    """
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
        remaind=Count("id", filter=Q(answered=False)),
        correct=Count("id", filter=Q(correct_answered=True)),
        wrong=Count("id", filter=Q(correct_answered=False) & Q(answered=True)),
    )

    data = {"detail": results_by_category, "general": general_results}

    return render(request, "school/challenges/resume.html", {"data": data})
