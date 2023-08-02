from django.test import TransactionTestCase
from ...models import UserProfile
from django.core.exceptions import ValidationError


class UserProfileTestCase(TransactionTestCase):
    fixtures = ["users_data.json", "userprofile_data.json"]

    def __init__(self):
        self.volunteer = None

    def setup(self):
        self.volunteer = UserProfile.objects.get(email='volunteer@example.com')

    # def test_userprofile_is_pending(self):
    #     user_profile = UserProfile(user=None, status=UserProfile.PENDING)
    #     self.assertIs(user_profile.is_pending(), True)
