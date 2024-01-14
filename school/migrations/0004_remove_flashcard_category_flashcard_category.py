# Generated by Django 5.0.1 on 2024-01-14 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_delete_flashcardlevel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='category',
        ),
        migrations.AddField(
            model_name='flashcard',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='flascards', to='school.flashcardcategory'),
            preserve_default=False,
        ),
    ]
