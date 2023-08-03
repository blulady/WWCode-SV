from django.test import TransactionTestCase
from ...models import UserProfile
from django.core.exceptions import ValidationError


class TestUserProfile(TransactionTestCase):
    reset_sequences = True
    fixtures = ["users_data.json", "userprofile_data.json", "roles_data.json", "teams_data.json"]
    volunteer_brenda = None
    volunteer_sophie = None
    volunteer_alexander = None

    def test_brendaprofile(self):
        self.volunteer_brenda = UserProfile.objects.get(user='5')
        self.assertEqual(self.volunteer_brenda.status, 'ACTIVE')
        self.assertEqual(self.volunteer_brenda.city, 'San Diego')
        self.assertEqual(self.volunteer_brenda.state, 'ca')
        self.assertEqual(self.volunteer_brenda.country, 'United States')
        self.assertEqual(self.volunteer_brenda.Timezone, None)
        self.assertGreater(len(self.volunteer_brenda.Bio), 2000)
        self.assertFalse(self.volunteer_brenda.Photo)
        self.assertFalse(self.volunteer_brenda.Slack_Handle)
        self.assertEqual(self.volunteer_brenda.LinkedIn, "https://www.linkedin.com/in/brendajackson")
        self.assertEqual(self.volunteer_brenda.Instagram, "https://instagram.com/brendajackson?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_brenda.Facebook, "https://www.facebook.com/brenda.jackson.23")
        self.assertEqual(self.volunteer_brenda.Twitter, "https://fosstodon.org/@BrendaJackson")
        self.assertEqual(self.volunteer_brenda.Medium, "https://medium.com/@brendajackson")

    def test_sophieprofile(self):
        self.volunteer_sophie = UserProfile.objects.get(user='6')
        self.assertEqual(self.volunteer_sophie.status, 'ACTIVE')
        self.assertEqual(self.volunteer_sophie.city, 'San Jose')
        self.assertEqual(self.volunteer_sophie.state, 'ca')
        self.assertEqual(self.volunteer_sophie.country, 'United States')
        self.assertEqual(self.volunteer_sophie.Timezone, 'PST')
        self.assertFalse(self.volunteer_sophie.Bio)
        self.assertEqual(self.volunteer_sophie.Photo, "images/tira_token_BAhKrZP.png")
        self.assertFalse(self.volunteer_sophie.Slack_Handle)
        self.assertEqual(self.volunteer_sophie.LinkedIn, "https://www.linkedin.com/in/sophiefisher/")
        self.assertEqual(self.volunteer_sophie.Instagram, "https://instagram.com/sophiefishes?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_sophie.Facebook, "https://www.facebook.com/sophiefisher.35")
        self.assertEqual(self.volunteer_sophie.Twitter, "https://www.twitter.com/SophieFisher23")
        self.assertFalse(self.volunteer_sophie.Medium)

    def test_alexanderprofile(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        self.assertEqual(self.volunteer_alexander.status, 'ACTIVE')
        self.assertEqual(self.volunteer_alexander.city, 'San Francisco')
        self.assertEqual(self.volunteer_alexander.state, 'CA')
        self.assertEqual(self.volunteer_alexander.country, 'United States')
        self.assertEqual(self.volunteer_alexander.Timezone, 'PST')
        self.assertFalse(self.volunteer_alexander.Bio)
        self.assertEqual(self.volunteer_alexander.Photo, "images/kettle1_g66bkO7.jpg")
        self.assertFalse(self.volunteer_alexander.Slack_Handle)
        self.assertEqual(self.volunteer_alexander.LinkedIn, "https://www.linkedin.com/in/alexanderbrown/")
        self.assertEqual(self.volunteer_alexander.Instagram, "https://instagram.com/alexanderbrown?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_alexander.Facebook, "https://www.facebook.com/alexanderbrown")
        self.assertEqual(self.volunteer_alexander.Twitter, "https://mstdn.social/@alexanderbrown")
        self.assertFalse(self.volunteer_alexander.Medium)

    def test_field_labels(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        city_field_label = self.volunteer_alexander._meta.get_field('city').verbose_name
        state_field_label = self.volunteer_alexander._meta.get_field('state').verbose_name
        country_field_label = self.volunteer_alexander._meta.get_field('country').verbose_name
        timezone_field_label = self.volunteer_alexander._meta.get_field('Timezone').verbose_name
        bio_field_label = self.volunteer_alexander._meta.get_field('Bio').verbose_name
        photo_field_label = self.volunteer_alexander._meta.get_field('Photo').verbose_name
        slack_handle_field_label = self.volunteer_alexander._meta.get_field('Slack_Handle').verbose_name
        linkedin_field_label = self.volunteer_alexander._meta.get_field('LinkedIn').verbose_name
        instagram_field_label = self.volunteer_alexander._meta.get_field('Instagram').verbose_name
        facebook_field_label = self.volunteer_alexander._meta.get_field('Facebook').verbose_name
        twitter_field_label = self.volunteer_alexander._meta.get_field('Twitter').verbose_name
        medium_field_label = self.volunteer_alexander._meta.get_field('Medium').verbose_name
        self.assertEqual(city_field_label, 'city')
        self.assertEqual(state_field_label, 'state')
        self.assertEqual(country_field_label, 'country')
        self.assertEqual(timezone_field_label, 'Timezone')
        self.assertEqual(bio_field_label, 'Bio')
        self.assertEqual(photo_field_label, 'Photo')
        self.assertEqual(slack_handle_field_label, 'Slack Handle')
        self.assertEqual(linkedin_field_label, 'LinkedIn')
        self.assertEqual(instagram_field_label, 'Instagram')
        self.assertEqual(facebook_field_label, 'Facebook')
        self.assertEqual(twitter_field_label, 'Twitter')
        self.assertEqual(medium_field_label, 'Medium')

    def test_fields_length(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        city_field_length = self.volunteer_alexander._meta.get_field('city').max_length
        state_field_length = self.volunteer_alexander._meta.get_field('state').max_length
        country_field_length = self.volunteer_alexander._meta.get_field('country').max_length
        timezone_field_length = self.volunteer_alexander._meta.get_field('Timezone').max_length
        slack_handle_field_length = self.volunteer_alexander._meta.get_field('Slack_Handle').max_length
        linkedin_field_length = self.volunteer_alexander._meta.get_field('LinkedIn').max_length
        instagram_field_length = self.volunteer_alexander._meta.get_field('Instagram').max_length
        facebook_field_length = self.volunteer_alexander._meta.get_field('Facebook').max_length
        twitter_field_length = self.volunteer_alexander._meta.get_field('Twitter').max_length
        medium_field_length = self.volunteer_alexander._meta.get_field('Medium').max_length

        self.assertEqual(city_field_length, 255)
        self.assertEqual(state_field_length, 255)
        self.assertEqual(country_field_length, 255)
        self.assertEqual(timezone_field_length, 255)
        self.assertEqual(slack_handle_field_length, 255)
        self.assertEqual(linkedin_field_length, 255)
        self.assertEqual(instagram_field_length, 255)
        self.assertEqual(facebook_field_length, 255)
        self.assertEqual(twitter_field_length, 255)
        self.assertEqual(medium_field_length, 255)

    def test_bio_length(self):
        self.volunteer = UserProfile.objects.get(user=1)
        self.volunteer.Bio = "test"  # Bio is too short
        with self.assertRaises(ValidationError):
            self.volunteer.full_clean()
