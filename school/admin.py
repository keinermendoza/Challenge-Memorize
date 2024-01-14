from django.contrib import admin
from school.models import FlashCard, FlashcardCategory, FlashCardAnswerOptions


@admin.register(FlashcardCategory)
class FlashcardCategoryAdmin(admin.ModelAdmin):
    pass

class FlashCardAnswerOptionsInline(admin.TabularInline):
    extra = 2
    model = FlashCardAnswerOptions

@admin.register(FlashCard)
class FLashCardAdmin(admin.ModelAdmin):

    list_display = ["shorted_question", "category", "level"]
    inlines = [FlashCardAnswerOptionsInline]
    

    