from django.test import TransactionTestCase
from ...models import UserProfile


class TestUserProfile(TransactionTestCase):
    reset_sequences = True
    fixtures = ["users_data.json", "roles_data.json", "teams_data.json"]
    volunteer_brenda = None
    volunteer_sophie = None
    volunteer_alexander = None

    def test_brendaprofile(self):
        self.volunteer_brenda = UserProfile.objects.get(user='5')
        self.assertEqual(self.volunteer_brenda.status, 'ACTIVE')
        self.assertEqual(self.volunteer_brenda.city, 'San Diego')
        self.assertEqual(self.volunteer_brenda.state, 'ca')
        self.assertEqual(self.volunteer_brenda.country, 'United States')
        self.assertEqual(self.volunteer_brenda.timezone, None)
        self.assertFalse(self.volunteer_brenda.photo)
        self.assertFalse(self.volunteer_brenda.slack_handle)
        self.assertEqual(self.volunteer_brenda.linkedin, "https://www.linkedin.com/in/brendajackson")
        self.assertEqual(self.volunteer_brenda.instagram, "https://instagram.com/brendajackson?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_brenda.facebook, "https://www.facebook.com/brenda.jackson.23")
        self.assertEqual(self.volunteer_brenda.twitter, "https://fosstodon.org/@BrendaJackson")
        self.assertEqual(self.volunteer_brenda.medium, "https://medium.com/@brendajackson")

    def test_sophieprofile(self):
        self.volunteer_sophie = UserProfile.objects.get(user='6')
        self.assertEqual(self.volunteer_sophie.status, 'ACTIVE')
        self.assertEqual(self.volunteer_sophie.city, 'San Jose')
        self.assertEqual(self.volunteer_sophie.state, 'ca')
        self.assertEqual(self.volunteer_sophie.country, 'United States')
        self.assertEqual(self.volunteer_sophie.timezone, 'PST')
        self.assertFalse(self.volunteer_sophie.bio)
        self.assertEqual(self.volunteer_sophie.photo, "images/tira_token_BAhKrZP.png")
        self.assertFalse(self.volunteer_sophie.slack_handle)
        self.assertEqual(self.volunteer_sophie.linkedin, "https://www.linkedin.com/in/sophiefisher/")
        self.assertEqual(self.volunteer_sophie.instagram, "https://instagram.com/sophiefishes?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_sophie.facebook, "https://www.facebook.com/sophiefisher.35")
        self.assertEqual(self.volunteer_sophie.twitter, "https://www.twitter.com/SophieFisher23")
        self.assertFalse(self.volunteer_sophie.medium)

    def test_alexanderprofile(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        self.assertEqual(self.volunteer_alexander.status, 'ACTIVE')
        self.assertEqual(self.volunteer_alexander.city, 'San Francisco')
        self.assertEqual(self.volunteer_alexander.state, 'CA')
        self.assertEqual(self.volunteer_alexander.country, 'United States')
        self.assertEqual(self.volunteer_alexander.timezone, 'PST')
        self.assertFalse(self.volunteer_alexander.bio)
        self.assertEqual(self.volunteer_alexander.photo, "images/kettle1_g66bkO7.jpg")
        self.assertFalse(self.volunteer_alexander.slack_handle)
        self.assertEqual(self.volunteer_alexander.linkedin, "https://www.linkedin.com/in/alexanderbrown/")
        self.assertEqual(self.volunteer_alexander.instagram, "https://instagram.com/alexanderbrown?igshid=MzRlODBiNWFlZA==")
        self.assertEqual(self.volunteer_alexander.facebook, "https://www.facebook.com/alexanderbrown")
        self.assertEqual(self.volunteer_alexander.twitter, "https://mstdn.social/@alexanderbrown")
        self.assertFalse(self.volunteer_alexander.medium)

    def test_field_labels(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        city_field_label = self.volunteer_alexander._meta.get_field('city').verbose_name
        state_field_label = self.volunteer_alexander._meta.get_field('state').verbose_name
        country_field_label = self.volunteer_alexander._meta.get_field('country').verbose_name
        timezone_field_label = self.volunteer_alexander._meta.get_field('timezone').verbose_name
        bio_field_label = self.volunteer_alexander._meta.get_field('bio').verbose_name
        photo_field_label = self.volunteer_alexander._meta.get_field('photo').verbose_name
        slack_handle_field_label = self.volunteer_alexander._meta.get_field('slack_handle').verbose_name
        linkedin_field_label = self.volunteer_alexander._meta.get_field('linkedin').verbose_name
        instagram_field_label = self.volunteer_alexander._meta.get_field('instagram').verbose_name
        facebook_field_label = self.volunteer_alexander._meta.get_field('facebook').verbose_name
        twitter_field_label = self.volunteer_alexander._meta.get_field('twitter').verbose_name
        medium_field_label = self.volunteer_alexander._meta.get_field('medium').verbose_name
        self.assertEqual(city_field_label, 'city')
        self.assertEqual(state_field_label, 'state')
        self.assertEqual(country_field_label, 'country')
        self.assertEqual(timezone_field_label, 'timezone')
        self.assertEqual(bio_field_label, 'bio')
        self.assertEqual(photo_field_label, 'photo')
        self.assertEqual(slack_handle_field_label, 'slack handle')
        self.assertEqual(linkedin_field_label, 'linkedin')
        self.assertEqual(instagram_field_label, 'instagram')
        self.assertEqual(facebook_field_label, 'facebook')
        self.assertEqual(twitter_field_label, 'twitter')
        self.assertEqual(medium_field_label, 'medium')

    def test_fields_length(self):
        self.volunteer_alexander = UserProfile.objects.get(user='7')
        city_field_length = self.volunteer_alexander._meta.get_field('city').max_length
        state_field_length = self.volunteer_alexander._meta.get_field('state').max_length
        country_field_length = self.volunteer_alexander._meta.get_field('country').max_length
        timezone_field_length = self.volunteer_alexander._meta.get_field('timezone').max_length
        slack_handle_field_length = self.volunteer_alexander._meta.get_field('slack_handle').max_length
        linkedin_field_length = self.volunteer_alexander._meta.get_field('linkedin').max_length
        instagram_field_length = self.volunteer_alexander._meta.get_field('instagram').max_length
        facebook_field_length = self.volunteer_alexander._meta.get_field('facebook').max_length
        twitter_field_length = self.volunteer_alexander._meta.get_field('twitter').max_length
        medium_field_length = self.volunteer_alexander._meta.get_field('medium').max_length

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
