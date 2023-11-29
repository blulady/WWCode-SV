from django.test import TransactionTestCase
from ...models import Mentor


class TestMentor(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'roles_data.json', 'teams_data.json', 'mentor_data.json']
    mentor_raquel = None
    mentor_kelly = None
    mentor_sammy = None

    def test_raquelmentor(self):
        self.mentor_raquel = Mentor.objects.get(pk=1)
        self.assertEqual(self.mentor_raquel.first_name, 'Raquel')
        self.assertEqual(self.mentor_raquel.last_name, 'Nunoz')
        self.assertEqual(self.mentor_raquel.email, 'raquelnunoz@email.com')
        self.assertEqual(self.mentor_raquel.level, "Beginner")
        self.assertEqual(self.mentor_raquel.reliability, "Unknown")

    def test_kellymentor(self):
        self.mentor_kelly = Mentor.objects.get(pk=2)
        self.assertEqual(self.mentor_kelly.first_name, 'Kelly')
        self.assertEqual(self.mentor_kelly.last_name, 'Apple')
        self.assertEqual(self.mentor_kelly.email, 'kellyapple@example.com')
        self.assertEqual(self.mentor_kelly.level, "Beginner")
        self.assertEqual(self.mentor_kelly.reliability, "Unknown")

    def test_sammymentor(self):
        self.mentor_sammy = Mentor.objects.get(pk=3)
        self.assertEqual(self.mentor_sammy.first_name, 'Sammy')
        self.assertEqual(self.mentor_sammy.last_name, 'Smith')
        self.assertEqual(self.mentor_sammy.email, 'ssmith@example.com')
        self.assertEqual(self.mentor_sammy.level, "Intermediate")
        self.assertEqual(self.mentor_sammy.reliability, "Poor")

    def test_field_labels(self):
        self.mentor_raquel = Mentor.objects.get(pk=1)
        first_name_field = self.mentor_raquel._meta.get_field('first_name').verbose_name
        last_name_field = self.mentor_raquel._meta.get_field('last_name').verbose_name
        email_field = self.mentor_raquel._meta.get_field('email').verbose_name
        level_field = self.mentor_raquel._meta.get_field('level').verbose_name
        reliability_field = self.mentor_raquel._meta.get_field('reliability').verbose_name
        self.assertEqual(first_name_field, 'first name')
        self.assertEqual(last_name_field, 'last name')
        self.assertEqual(email_field, 'email')
        self.assertEqual(level_field, 'level')
        self.assertEqual(reliability_field, 'reliability')

    def test_field_lengths(self):
        self.mentor_raquel = Mentor.objects.get(pk=1)
        first_name_field = self.mentor_raquel._meta.get_field('first_name').max_length
        last_name_field = self.mentor_raquel._meta.get_field('last_name').max_length
        email_field = self.mentor_raquel._meta.get_field('email').max_length
        level_field = self.mentor_raquel._meta.get_field('level').max_length
        reliability_field = self.mentor_raquel._meta.get_field('reliability').max_length
        self.assertEqual(first_name_field, 255)
        self.assertEqual(last_name_field, 255)
        self.assertEqual(email_field, 255)
        self.assertEqual(level_field, 20)
        self.assertEqual(reliability_field, 20)
