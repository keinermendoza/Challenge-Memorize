from django.contrib import admin
from school.custom_admin import CustomAdmin
from school.models import (
    FlashCard,
    StudyCategory,
    Challenge,
    ChallengeQuestion
)


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
