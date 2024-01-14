from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
class FlashcardCategory(models.Model): # fcat
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(
            fields=["name"]
        )]
    def __str__(self):
        return self.name

class FlashCard(models.Model): # f
    class Level(models.IntegerChoices):
        EASY = (1, 'Easy')
        NORMAL = (2, 'Normal')
        HARD = (3, 'Hard')
        MASTER = (4, 'Master')

    question = models.CharField(max_length=100)
    category = models.ForeignKey(FlashcardCategory ,related_name="flashcards", on_delete=models.CASCADE, null=True)
    level = models.IntegerField(choices=Level.choices, default=Level.NORMAL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def shorted_question(self):
        return Truncator(text=self.question).words(num=6)

    def __str__(self):
        return self.shorted_question

    
    def get_absolute_url(self):
        return reverse("flashcards", args={"pk": self.pk})
        
   
    
    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(
            fields=["-created"]
        )]

class FlashCardAnswerOptions(models.Model): #f opt
    option = models.CharField(max_length=100)
    right = models.BooleanField(default=False)
    question = models.ForeignKey(FlashCard, related_name="option", on_delete=models.CASCADE, blank=True)


