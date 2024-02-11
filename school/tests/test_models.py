from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from school.models import FlashCard, StudyCategory


class StudyCategoryTest(TestCase):
    @classmethod
    def setUpTestData(self):
        StudyCategory.objects.create(name="python")

    def test_category_created(self):
        python_category = StudyCategory.objects.get(id=1)
        self.assertIsInstance(python_category, StudyCategory)

    def test_category_str(self):
        python_category = StudyCategory.objects.get(id=1)
        self.assertEqual(python_category.__str__(), "python")

    def test_category_creation(self):
        rust_creation = StudyCategory.objects.create(name="rust")

        self.assertIsInstance(rust_creation, StudyCategory)
        self.assertEqual(StudyCategory.objects.count(), 2)

    def test_category_name_unique(self):
        with self.assertRaises(IntegrityError):
            StudyCategory.objects.create(name="python")


class FlasCardTests(TestCase):
    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        user = User.objects.create_user(email="norman@gmail.com", password="password")

        html_category = StudyCategory.objects.create(name="HTML")
        FlashCard.objects.create(
            user=user,
            category=html_category,
            question="what is the most used MARKUP Language in web development",
            answer="HTML",
        )

    def test_flashcard_created(self):
        flashcard = FlashCard.objects.get(id=1)
        self.assertIsInstance(flashcard, FlashCard)
        self.assertEqual(flashcard.level, FlashCard.Level.NORMAL)

    def test_create_flashcard_without_category(self):
        User = get_user_model()
        user = User.objects.get(id=1)
        flashcard = FlashCard.objects.create(
            user=user, question="what is the best programming lenguage", answer="python"
        )

        self.assertIsInstance(flashcard, FlashCard)

    def test_create_flashcard_require_user(self):
        with self.assertRaises(IntegrityError):
            FlashCard.objects.create(
                question="what is the best programming lenguage", answer="python"
            )

    def test_flashcard_str(self):
        flashcard = FlashCard.objects.get(id=1)
        self.assertEqual(flashcard.__str__(), "what is the most used markup …")


class ChallengeTests(TestCase):
    pass
