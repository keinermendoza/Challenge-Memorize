from django.contrib import admin
from school.models import FlashCard, ChoicesCard, StudyCategory, ChoicesCardAnswerOptions

@admin.register(StudyCategory)
class ChoicesCardCategoryAdmin(admin.ModelAdmin):
    pass

class ChoicesCardAnswerOptionsInline(admin.TabularInline):
    extra = 2
    model = ChoicesCardAnswerOptions

@admin.register(ChoicesCard)
class ChoicesCardAdmin(admin.ModelAdmin):

    list_display = ["shorted_question", "category", "level"]
    inlines = [ChoicesCardAnswerOptionsInline]
    
admin.site.register(FlashCard)
