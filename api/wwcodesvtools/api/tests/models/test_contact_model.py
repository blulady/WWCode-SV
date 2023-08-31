from api.models import Contact, Host, User
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase


class ContactModelTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json']
    _volunteer = None

    def setUp(self):
        self._volunteer = User.objects.get(email='volunteer@example.com')
        host = Host(company='WWC-SV', created_by=self._volunteer, updated_by=self._volunteer)
        host.save()
        self._host = Host.objects.last()

    # test name max length
    def test_name_max_length(self):
        test_name = 'a' * 256
        contact = Contact(name=test_name, email="test_email@test.com", company=self._host)
        with self.assertRaises(ValidationError) as error:
            contact.full_clean()
            expected_error_message = f"Ensure this value has at most 255 characters (it has {len(test_name)} characters)."
            self.assertEqual(error.exception.error_dict["name"][0].message, expected_error_message)

    # test email max length
    def test_email_max_length(self):
        test_email = 'a'*255
        contact = Contact(name="test_name", email=test_email, company=self._host)
        with self.assertRaises(ValidationError) as error:
            contact.full_clean()
            expected_error_message = f"Ensure this value has at most 254 characters (it has {len(test_email)} characters)."
            self.assertEqual(error.exception.error_dict["email"][0].message, expected_error_message)

    # test info max length
    def test_info_max_length(self):
        test_info = 'a'*2001
        contact = Contact(name="test_name", email="test_email@test.com", info=test_info, company=self._host)
        with self.assertRaises(ValidationError) as error:
            contact.full_clean()
            expected_error_message = f"Ensure this value has at most 2000 characters (it has {len(test_info)} characters)."
            self.assertEqual(error.exception.error_dict["info"][0].message, expected_error_message)

    # test relation to Host table
    def test_host(self):
        contact = Contact(name="test_name", email="test_email@test.com", company=self._host)
        contact.save()

        self.assertEqual(contact.company, Host.objects.get(pk=1))
