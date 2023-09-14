from django.test import TransactionTestCase
from ...models import Mentor


class TestMentor(TransactionTestCase):
    reset_sequences = True
    fixtures = ['mentor_data.json']
    mentor_viri = None
    mentor_marisia = None
    mentor_kelly = None

    def test_virimentor(self):
        self.mentor_viri = Mentor.objects.get(pk=1)
        self.assertEqual(self.mentor_viri.first_name, 'Viri')
        self.assertEqual(self.mentor_viri.last_name, 'Ponce')
        self.assertEqual(self.mentor_viri.email, 'viriponce@example.com')
        self.assertEqual(self.mentor_viri.level, "Advanced")
        self.assertEqual(self.mentor_viri.reliability, "Excellent")

    def test_marisiamentor(self):
        self.mentor_marisia = Mentor.objects.get(pk=2)
        self.assertEqual(self.mentor_marisia.first_name, 'Marisia')
        self.assertEqual(self.mentor_marisia.last_name, 'Sanjuan')
        self.assertEqual(self.mentor_marisia.email, 'msanjuan@example.com')
        self.assertEqual(self.mentor_marisia.level, "Advanced")
        self.assertEqual(self.mentor_marisia.reliability, "Excellent")

    def test_kellymentor(self):
        self.mentor_kelly = Mentor.objects.get(pk=3)
        self.assertEqual(self.mentor_kelly.first_name, 'Kelly')
        self.assertEqual(self.mentor_kelly.last_name, 'Apple')
        self.assertEqual(self.mentor_kelly.email, 'kellyapple@example.com')
        self.assertEqual(self.mentor_kelly.level, "Intermediate")
        self.assertEqual(self.mentor_kelly.reliability, "Unknown")

    def test_field_labels(self):
        self.mentor_viri = Mentor.objects.get(pk=1)
        first_name_field = self.mentor_viri._meta.get_field('first_name').verbose_name
        last_name_field = self.mentor_viri._meta.get_field('last_name').verbose_name
        email_field = self.mentor_viri._meta.get_field('email').verbose_name
        level_field = self.mentor_viri._meta.get_field('level').verbose_name
        reliability_field = self.mentor_viri._meta.get_field('reliability').verbose_name
        self.assertEqual(first_name_field, 'first name')
        self.assertEqual(last_name_field, 'last name')
        self.assertEqual(email_field, 'email')
        self.assertEqual(level_field, 'level')
        self.assertEqual(reliability_field, 'reliability')

    def test_field_lengths(self):
        self.mentor_viri = Mentor.objects.get(pk=1)
        first_name_field = self.mentor_viri._meta.get_field('first_name').max_length
        last_name_field = self.mentor_viri._meta.get_field('last_name').max_length
        email_field = self.mentor_viri._meta.get_field('email').max_length
        level_field = self.mentor_viri._meta.get_field('level').max_length
        reliability_field = self.mentor_viri._meta.get_field('reliability').max_length
        self.assertEqual(first_name_field, 255)
        self.assertEqual(last_name_field, 255)
        self.assertEqual(email_field, 255)
        self.assertEqual(level_field, 20)
        self.assertEqual(reliability_field, 20)
