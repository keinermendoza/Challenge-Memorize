# Generated by Django 5.0.1 on 2024-01-19 15:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_flashcard_answer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='flashcards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('level', models.IntegerField(choices=[(1, 'Easy'), (2, 'Normal'), (3, 'Hard'), (4, 'Master')], default=2)),
                ('status', models.IntegerField(choices=[(0, 'In Process'), (1, 'Complete')], default=0)),
                ('number_questions', models.PositiveIntegerField()),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.BooleanField(default=False)),
                ('correct_answered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.challenge')),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.flashcard')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='questions',
            field=models.ManyToManyField(through='school.ChallengeQuestion', to='school.flashcard'),
        ),
    ]
