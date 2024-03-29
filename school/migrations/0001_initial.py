# Generated by Django 5.0.1 on 2024-02-10 18:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Challenge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "level",
                    models.IntegerField(
                        choices=[
                            (1, "Easy"),
                            (2, "Normal"),
                            (3, "Hard"),
                            (4, "Master"),
                        ],
                        default=2,
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "In Process"), (1, "Complete")], default=0
                    ),
                ),
                (
                    "number_questions",
                    models.PositiveIntegerField(
                        verbose_name="Maximun number of questions"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenges",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FlashCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=100)),
                (
                    "level",
                    models.IntegerField(
                        choices=[
                            (1, "Easy"),
                            (2, "Normal"),
                            (3, "Hard"),
                            (4, "Master"),
                        ],
                        default=2,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("answer", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flashcards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="ChallengeQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answered", models.BooleanField(default=False)),
                ("correct_answered", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenge_questions",
                        to="school.challenge",
                    ),
                ),
                (
                    "flashcard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenge_questions",
                        to="school.flashcard",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="challenge",
            name="questions",
            field=models.ManyToManyField(
                through="school.ChallengeQuestion", to="school.flashcard"
            ),
        ),
        migrations.CreateModel(
            name="StudyCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["name"], name="school_stud_name_182a5e_idx")
                ],
            },
        ),
        migrations.AddField(
            model_name="flashcard",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flashcards",
                to="school.studycategory",
            ),
        ),
        migrations.AddField(
            model_name="challenge",
            name="categories",
            field=models.ManyToManyField(
                related_name="challenges", to="school.studycategory"
            ),
        ),
        migrations.AddIndex(
            model_name="flashcard",
            index=models.Index(
                fields=["-created"], name="school_flas_created_76eaeb_idx"
            ),
        ),
    ]
