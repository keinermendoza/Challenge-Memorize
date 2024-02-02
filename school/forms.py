import copy
from django import forms
from django.core.validators import MaxValueValidator

from school.models import (
    StudyCategory,
    FlashCard,
    Challenge,
    ChallengeQuestion,
)

CATEGORIES = list(StudyCategory.objects.all().values_list("id", "name"))
CATEGORIES.insert(0, ("", "All Categories"))
LEVELS = FlashCard.Level.choices
LEVELS.insert(0, ("", "All Levels"))
STATUS = Challenge.Status.choices
STATUS.insert(0, ("", "All Status"))



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
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CATEGORIES)

    class Meta:
        model = Challenge
        fields = ["title", "level", "number_questions", "category"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        flashcard_num = request.user.flashcards.count()
        super(ChallengeForm, self).__init__(*args, **kwargs)

        # add validation
        self.fields["number_questions"].validators.append(
            MaxValueValidator(flashcard_num)
        )
        # add html max attribute
        self.fields["number_questions"].widget.attrs["max"] = flashcard_num
        
        # the categories in normal level that user has
        self.fields['category'].choices = StudyCategory.objects.filter(flashcards__user=request.user).filter(flashcards__level=2).distinct().values_list("id", "name")


class category_field_partial(forms.Form):
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                      queryset=StudyCategory.objects.none())
    
    def __init__(self, *args, level=None, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

        if level is not None:
            self.fields['category'].queryset = StudyCategory.objects.filter(
                flashcards__level=level
            ).distinct() 
    
    def clean_category(self):
        cd = super().clean()
        flashcards_in_categories = self.request.user.flashcards.filter(category__in=cd['category']).count()
        if len(cd['category']) != flashcards_in_categories:
            raise forms.ValidationError("please select only valid categories") 
        return cd['category']
    
