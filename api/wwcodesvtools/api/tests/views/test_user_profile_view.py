from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from api.models import User, UserProfile
import json


class UserProfileViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'userprofile_data.json']
    USERPROFILE_FIELDS = ['city', 'state', 'country', 'timezone', 'bio', 'photo', 'slack_handle', 'linkedin', 'instagram', 'facebook', 'twitter', 'medium']
    VOLUNTEER_EMAIL = 'volunteer@example.com'
    PASSWORD = 'Password123'

    def setUp(self):
        self.access_token = self.get_token(self.VOLUNTEER_EMAIL, self.PASSWORD)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Get complete user information of volunteer
    def test_get_user_profile_info(self):
        response = self.client.get("/api/user/profile/", **self.bearer)
        responseLength = len(response.data)
        user_profile = json.loads(response.content)
        self.assertEqual(responseLength, 20)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_profile['first_name'], "alice")
        self.assertEqual(user_profile['last_name'], "robinson")
        self.assertEqual(user_profile['email'], self.VOLUNTEER_EMAIL)
        self.assertEqual(user_profile['highest_role'], "VOLUNTEER")
        self.assertEqual(len(user_profile['role_teams']), 3)
        for k in self.USERPROFILE_FIELDS:
            self.assertEqual(user_profile[k], None)

    # Update only information from the user table
    def test_update_only_first_name_and_last_name(self):
        json_type = "application/json"
        data = json.dumps({'first_name': 'Alice',
                           'last_name': 'Robinson',
                           'city': "",
                           'state': "",
                           'country': "",
                           'timezone': "",
                           'bio': "",
                           'photo': "",
                           'slack_handle': "",
                           'linkedin': "",
                           'instagram': "",
                           'facebook': "",
                           'twitter': "",
                           'medium': "",
                           })
        response = self.client.put("/api/user/profile/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Robinson")
        user_profile = UserProfile.objects.filter(user_id=2)
        self.assertEqual(len(user_profile), 1)
        for k in self.USERPROFILE_FIELDS:
            self.assertEqual(getattr(user_profile[0], k), "")

    # Update only some information from the user_profile table
    def test_update_user_profile_table(self):
        json_type = "application/json"
        data = json.dumps({'first_name': 'alice',
                           'last_name': 'robinson',
                           'city': "Mountain View",
                           'state': "CA",
                           'country': "USA",
                           'timezone': "",
                           'bio': "",
                           'photo': "",
                           'slack_handle': "",
                           'linkedin': "",
                           'instagram': "",
                           'facebook': "",
                           'twitter': "",
                           'medium': "",
                           })
        response = self.client.put("/api/user/profile/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "alice")
        self.assertEqual(user.last_name, "robinson")
        user_profile = UserProfile.objects.get(user_id=2)
        for k in self.USERPROFILE_FIELDS:
            if k not in ['city', 'state', 'country']:
                self.assertEqual(getattr(user_profile, k), "")
        self.assertEqual(user_profile.city, "Mountain View")
        self.assertEqual(user_profile.state, "CA")
        self.assertEqual(user_profile.country, "USA")

    # Update all information
    def test_update_complete_user_profile(self):
        json_type = "application/json"
        profile_data = {'first_name': 'Alice',
                        'last_name': 'Robinson'}
        for k in self.USERPROFILE_FIELDS:
            profile_data[k] = k
        data = profile_data
        response = self.client.put("/api/user/profile/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Robinson")
        user_profile = UserProfile.objects.get(user_id=2)
        for k in self.USERPROFILE_FIELDS:
            self.assertEqual(getattr(user_profile, k), k)
