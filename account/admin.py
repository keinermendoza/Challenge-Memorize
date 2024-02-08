from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from school.custom_admin import CustomAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(CustomAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username", "is_staff", "is_active"]
    list_filter = []


    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

