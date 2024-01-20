from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from account.models import User

class StudyCategory(models.Model): # fcat
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(
            fields=["name"]
        )]
    def __str__(self):
        return self.name

class AbstractCard(models.Model):
    """BASE CLASS for inerith to FlashCard and ChoiceCard"""
    class Level(models.IntegerChoices):
        EASY = (1, 'Easy')
        NORMAL = (2, 'Normal')
        HARD = (3, 'Hard')
        MASTER = (4, 'Master')

    question = models.CharField(max_length=100)
    level = models.IntegerField(choices=Level.choices, default=Level.NORMAL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def shorted_question(self):
        return Truncator(text=self.question).words(num=6)

    def __str__(self):
        return self.shorted_question
    
    class Meta:
        abstract = True

class FlashCard(AbstractCard):
    answer = models.TextField()
    category = models.ForeignKey(StudyCategory ,related_name="flashcards", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="flashcards", on_delete=models.DO_NOTHING, blank=True)
    
    @property
    def is_multiple_choice(self):
        return False
    
    def get_absolute_url(self):
        return reverse("flashcards", args={"pk": self.pk})
    
    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(
            fields=["-created"]
        )]

class Challenge(models.Model):
    class Level(models.IntegerChoices):
        EASY = (1, 'Easy')
        NORMAL = (2, 'Normal')
        HARD = (3, 'Hard')
        MASTER = (4, 'Master')

    class Status(models.IntegerChoices):
        PROCESS = (0, 'In Process')
        COMPLETE = (1, 'Complete')

    title = models.CharField(max_length=100)
    level = models.IntegerField(choices=Level.choices, default=Level.NORMAL)
    status = models.IntegerField(choices=Status.choices, default=Status.PROCESS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    number_questions = models.PositiveIntegerField()
    questions = models.ManyToManyField(FlashCard, through='ChallengeQuestion')

class ChallengeQuestion(models.Model):
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE, related_name='challenge_questions') # name for acces
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_questions') # name for acces
    answered = models.BooleanField(default=False)
    correct_answered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_response_url(self):
        return reverse('school:challenge_answer', args=[self.id])
    
    def get_resume_url(self):
        return reverse('school:challenge_resume', args=[self.id])

class ChoicesCard(AbstractCard): # f
    category = models.ForeignKey(StudyCategory ,related_name="choicecards", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="choicecards", on_delete=models.DO_NOTHING)

    @property
    def is_multiple_choice(self):
        return True
    
    def get_absolute_url(self):
        return reverse("flashcards", args={"pk": self.pk})
    
    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(
            fields=["-created"]
        )]

class ChoicesCardAnswerOptions(models.Model): #f opt
    option = models.CharField(max_length=100)
    right = models.BooleanField(default=False)
    question = models.ForeignKey(ChoicesCard, related_name="option", on_delete=models.CASCADE, blank=True)


