from django import forms
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

from school.models import (
    StudyCategory,
    FlashCard,
    Challenge,
)

# TODO
# CATEGORIES = list(StudyCategory.objects.all().values_list("id", "name"))
# CATEGORIES.insert(0, ("", "All Categories"))
# LEVELS = FlashCard.Level.choices
# LEVELS.insert(0, ("", "All Levels"))
# STATUS = Challenge.Status.choices
# STATUS.insert(0, ("", "All Status"))

CATEGORIES = []
LEVELS = []
STATUS = []

class CategoryForm(forms.ModelForm):
    class Meta:
        model = StudyCategory
        fields = ["name"]

class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        exclude = ["user"]


class FilterChallengeForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES, required=False)
    level = forms.ChoiceField(choices=LEVELS, required=False)
    status = forms.ChoiceField(choices=STATUS, required=False)


class SearchFlashcardForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORIES, required=False)
    level = forms.ChoiceField(choices=LEVELS, required=False)
    question = forms.CharField(max_length=20, required=False)


class ChallengeForm(forms.ModelForm):
    """this form REQUIRES the request object"""

    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=[]
    )

    class Meta:
        model = Challenge
        fields = ["title", "level", "number_questions", "categories"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        flashcard_num = self.request.user.flashcards.count()
        super(ChallengeForm, self).__init__(*args, **kwargs)

        # add validation
        self.fields["number_questions"].validators.append(
            MaxValueValidator(flashcard_num)
        )
        # add html max attribute
        self.fields["number_questions"].widget.attrs["max"] = flashcard_num

        # all the categories associated with the user's flashcards
        user_categories = StudyCategory.objects.filter(
            flashcards__user=self.request.user
        ).distinct()
        self.fields["categories"].choices = user_categories.values_list("id", "name")

            
        # display only categories from 'normal' level for first render
        if len(self.data) == 0 or self.errors:
            self.fields["categories"].choices = (
                user_categories.filter(flashcards__level=2)
                .distinct()
                .values_list("id", "name")
            )

    def clean(self):
        cleaned_data = super().clean()
        category_match = Q(category__in=cleaned_data.get("categories", []))
        level_match = Q(level=cleaned_data.get("level", None))

        if not self.request.user.flashcards.filter(
            category_match,
            level_match
        ).count():
            raise ValidationError("You don't have flashcards with those specifications")
        
        return cleaned_data

class category_field_partial(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=StudyCategory.objects.none()
    )

    def __init__(self, *args, level=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop("request", None)

        if level is not None:
            self.fields["categories"].queryset = StudyCategory.objects.filter(
                flashcards__level=level
            ).distinct()

    def clean_category(self):
        cd = super().clean_category()
        flashcards_in_categories = self.request.user.flashcards.filter(
            category__in=cd["categories"]
        ).count()
        if len(cd["categories"]) != flashcards_in_categories:
            raise forms.ValidationError("please select only valid categories")
        return cd["categories"]
