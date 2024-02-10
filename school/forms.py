from django import forms
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

from school.models import (
    StudyCategory,
    FlashCard,
    Challenge,
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = StudyCategory
        fields = ["name"]

    def clean_name(self):
        if name := self.cleaned_data.get("name", None):
            if StudyCategory.objects.filter(name=name.lower()):
                raise forms.ValidationError(f"Sorry, the Category {name} is already registred") 
        return name     

class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        exclude = ["user"]


class FilterChallengeForm(forms.Form):
    category = forms.ChoiceField(choices=[], required=False)
    level = forms.ChoiceField(choices=[], required=False)
    status = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(FilterChallengeForm, self).__init__(*args, **kwargs)
        self.fields["category"].choices = StudyCategory.get_categories_tuple()
        self.fields["level"].choices = FlashCard.get_flashcard_levels_tuple()
        self.fields["status"].choices = Challenge.get_challenge_status_tuple()


class SearchFlashcardForm(forms.Form):
    category = forms.ChoiceField(choices=[], required=False)
    level = forms.ChoiceField(choices=[], required=False)
    question = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchFlashcardForm, self).__init__(*args, **kwargs)
        self.fields["category"].choices = StudyCategory.get_categories_tuple()
        self.fields["level"].choices = FlashCard.get_flashcard_levels_tuple()



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
        if categories := self.cleaned_data.get("categories", None):
            flashcards = self.request.user.flashcards
            flashcards_match_number = flashcards.filter(category__in=categories).count()
            
            if len(categories) != flashcards_match_number:
                raise forms.ValidationError("please select only valid categories")
            return categories
