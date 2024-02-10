from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from account.models import User

class StudyCategory(models.Model): 
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(
            fields=["name"]
        )]
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="category_name_constraint")
        ]

    def __str__(self):
        return self.name
    
    @classmethod
    def get_categories_tuple(cls):
        categories = list(cls.objects.all().values_list("id", "name"))
        categories.insert(0, ("", "All Categories"))
        return categories

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
        return Truncator(text=self.question).words(num=6, truncate=" …")

    def __str__(self):
        return self.shorted_question
    
    class Meta:
        abstract = True

class FlashCard(AbstractCard):
    answer = models.TextField()
    category = models.ForeignKey(StudyCategory ,related_name="flashcards", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="flashcards", on_delete=models.CASCADE, blank=True)
    
    @property
    def is_multiple_choice(self):
        return False


    @classmethod
    def get_flashcard_levels_tuple(cls):
        levels = cls.Level.choices
        levels.insert(0, ("", "All Levels"))
        return levels
    
    def save(self, *args, **kwargs):
        self.question = self.question.lower() 
        super(FlashCard, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(
            fields=["-created"]
        )]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "question",
                    "user"
                ],
                name="unique_flashcard_question_by_user_constraint")
        ]


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="challenges")
    number_questions = models.PositiveIntegerField("Maximun number of questions")
    questions = models.ManyToManyField(FlashCard, through='ChallengeQuestion')
    categories = models.ManyToManyField(StudyCategory, related_name="challenges")

    def __str__(self):
        return self.title

    def get_resume_url(self):
        return reverse('school:challenge_resume', args=[self.id])
    
    def get_start_challenge_url(self):
        return reverse('school:start_challenge', args=[self.id])
    
    @classmethod
    def get_challenge_status_tuple(cls):
        status = cls.Status.choices
        status.insert(0, ("", "All Status"))
        return status

class ChallengeQuestion(models.Model):
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE, related_name='challenge_questions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_questions')
    answered = models.BooleanField(default=False)
    correct_answered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_response_url(self):
        return reverse('school:challenge_answer', args=[self.id])
    
    def __str__(self):
        return f"#{self.id} from flashcard: {self.flashcard}"
    
