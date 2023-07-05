from api.models import Host, User
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase
from django.utils import timezone


class HostModelTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    _volunteer = None

    def setUp(self):
        self._volunteer = User.objects.get(email='volunteer@example.com')

    # test company name is not null
    def test_company_not_null(self):
        host = Host(company=None)
        with self.assertRaises(ValidationError) as error:
            host.full_clean()
            expected_error_message = "This field cannot be null."
            self.assertEqual(error.exception.error_dict["company"][0].message, expected_error_message)

    # test company name is unique
    def test_unique_company(self):
        host1 = Host(company='test_company', created_by=self._volunteer, updated_by=self._volunteer)
        host1.save()
        host2 = Host(company='test_company', created_by=self._volunteer, updated_by=self._volunteer)
        with self.assertRaises(ValidationError) as error:
            host2.full_clean()
            expected_error_message = "Host with this Company already exists."
            self.assertEqual(error.exception.error_dict["company"][0].message, expected_error_message)

    # test company name max length
    def test_company_max_length(self):
        test_company = 'a' * 256
        host = Host(company=test_company)
        with self.assertRaises(ValidationError) as error:
            host.full_clean()
            expected_error_message = f"Ensure this value has at most 255 characters (it has {len(test_company)} characters)."
            self.assertEqual(error.exception.error_dict["company"][0].message, expected_error_message)

    # test city name max length
    def test_city_max_length(self):
        test_city = 'a' * 256
        host = Host(city=test_city)
        with self.assertRaises(ValidationError) as error:
            host.full_clean()
            expected_error_message = f"Ensure this value has at most 255 characters (it has {len(test_city)} characters)."
            self.assertEqual(error.exception.error_dict["city"][0].message, expected_error_message)

    # test notes max length
    def test_notes_max_length(self):
        test_note = 'a'*2001
        host = Host(company='test_company', notes=test_note)
        with self.assertRaises(ValidationError) as error:
            host.full_clean()
            expected_error_message = f"Ensure this value has at most 2000 characters (it has {len(test_note)} characters)."
            self.assertEqual(error.exception.error_dict["notes"][0].message, expected_error_message)

    # test relation to User table
    def test_user(self):
        host = Host(company='WWC-SV', created_by=self._volunteer, updated_by=self._volunteer)
        host.save()

        self.assertEqual(host.created_by, User.objects.get(pk=2))

    # test timestamps
    def test_timestamps(self):
        host = Host(company='WWC-SV', created_by=self._volunteer, updated_by=self._volunteer)
        host.save()

        initial_created_at = host.created_at
        initial_updated_at = host.updated_at
        current_time = timezone.now()

        self.assertIsNotNone(initial_created_at)
        self.assertIsNotNone(initial_updated_at)
        self.assertLessEqual(initial_created_at, initial_updated_at)
        self.assertLessEqual(initial_updated_at, current_time)

        host.city = 'somewhere'
        host.save()

        new_created_at = host.created_at
        new_updated_at = host.updated_at

        self.assertEqual(initial_created_at, new_created_at)
        self.assertLess(initial_updated_at, new_updated_at)
