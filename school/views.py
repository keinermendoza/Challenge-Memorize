from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseForbidden, QueryDict
from django.db import IntegrityError

from django_htmx.http import retarget, reswap, trigger_client_event
from school.models import (
    StudyCategory,
    FlashCard,
)

from .forms import (
    FlashCardForm,
    SearchFlashcardForm,
    CategoryForm
)


def home(request):
    return render(request, "school/home.html")

@login_required
@require_http_methods(["POST"])
def category_create(request):
    """
        handles StudyCategory creation with CategoryForm throug htmx
        returns:
            - validation success: partial with category section to FlashCardForm
            - validation fails: CategoryForm with error messages
    """
    if not request.htmx:
        return HttpResponseForbidden()
    
    form = CategoryForm(request.POST)
    if form.is_valid():        
        form.save()
        
        categories = StudyCategory.objects.all()
        category_section = FlashCardForm(initial={'category':categories})
        response = render(request, "school/partials/forms/flashcard_create_sections/category.html", {"form": category_section})
        return trigger_client_event(response, "clean_errors")
    
    
    else:
        response = render(request, "school/partials/forms/category_create.html", {"form":form})
        return retarget(response, "#category-form-container")


@login_required
def flashcard_list(request):
    """
        GET: displays page with:
        - list of flashcards
        - FlashCardForm for handle creation
        - SearchCardForm for handle filtering
        - CategoryForm for handle category creation  
    """
    cards = FlashCard.objects.filter(user=request.user)
    flashcard_form = FlashCardForm()
    category_form = CategoryForm()
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
            return trigger_client_event(response, "clean_errors")

    return render(
        request,
        "school/flashcards.html",
        {"cards": cards, "flashcard_form": flashcard_form, "search_form": search_form, "category_form":category_form},
    )


@login_required
@require_http_methods(["POST"])
def flashcard_create(request):
    form = FlashCardForm(request.POST)

    if form.is_valid():
        flashcard = form.save(commit=False)
        flashcard.user = request.user
        try:
            flashcard.save()
            response = render(
                request,
                "school/partials/cards/detail.html",
                {"card": flashcard, "new_card": True},
            )
            return trigger_client_event(response, "fresh_flashcard_form")
        
        except IntegrityError:
            form.add_error("question", "You already registred this question")
            
    response = render(
        request,
        "school/partials/forms/create_flashcard.html",
        {"form": form},
    )
    response = reswap(response, "innerHTML")
    return retarget(response, "#flashcard-form-container")

@login_required
@require_http_methods(["GET"])
def fresh_flashcard_form(request):
    """
        Return a fresh instance of the flashcard form
    """
    if not request.htmx:
        return HttpResponseForbidden()
    form = FlashCardForm()
    return render(request, "school/partials/forms/create_flashcard.html", {"form":form})
    

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
            return trigger_client_event(response, "clean_errors")

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


