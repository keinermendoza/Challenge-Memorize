# Generated by Django 5.0.1 on 2024-02-10 20:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0002_studycategory_category_name_constraint"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="flashcard",
            constraint=models.UniqueConstraint(
                fields=("question", "user"),
                name="unique_flashcard_question_by_user_constraint",
            ),
        ),
    ]
