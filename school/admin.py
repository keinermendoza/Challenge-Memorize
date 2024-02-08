from django.contrib import admin
from school.custom_admin import CustomAdmin
from school.models import FlashCard, ChoicesCard, StudyCategory, ChoicesCardAnswerOptions\
    , Challenge, ChallengeQuestion


@admin.register(FlashCard)
class ChoicesCardAdmin(CustomAdmin):
    pass

@admin.register(Challenge)
class ChoicesCardAdmin(CustomAdmin):
    pass

@admin.register(ChallengeQuestion)
class ChoicesCardAdmin(CustomAdmin):
    pass

@admin.register(StudyCategory)
class ChoicesCardCategoryAdmin(CustomAdmin):
    pass


# class ChoicesCardAnswerOptionsInline(admin.TabularInline):
#     extra = 2
#     model = ChoicesCardAnswerOptions

# @admin.register(ChoicesCard)
# class ChoicesCardAdmin(CustomAdmin):

#     list_display = ["shorted_question", "category", "level"]
#     inlines = [ChoicesCardAnswerOptionsInline]
    
