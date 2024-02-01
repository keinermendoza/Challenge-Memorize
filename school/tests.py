from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from .models import FlashCard

class FlasCardTests(TestCase):

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        User.objects.create_user(email="norman@gmail.com", password="password")

    def test_create_flashcard_without_category(self):
        User = get_user_model()
        user = User.objects.get(id=1)
        flashcard = FlashCard.objects.create(user=user, question="what is the best programming lenguage", answer="python")
        self.assertIsInstance(flashcard, FlashCard)

    def test_create_flashcard_require_user(self):
        with self.assertRaises(IntegrityError):
            FlashCard.objects.create(question="what is the best programming lenguage", answer="python")
