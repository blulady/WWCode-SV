from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from api.models import Host, Contact
import json


class HostViewTestCase(TransactionTestCase):
    reset_sequences = True
    fixtures = ['users_data.json', 'teams_data.json', 'roles_data.json', 'hosts_data.json']
    DIRECTOR_EMAIL = 'director@example.com'
    NO_HOST_MANAGEMENT_EMAIL = 'leader@example.com'
    HOST_MANAGEMENT_EMAIL = 'volunteer@example.com'
    PASSWORD = 'Password123'

    def setUp(self):
        self.access_token = self.get_token(self.HOST_MANAGEMENT_EMAIL, self.PASSWORD)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: username,
            'password': password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Access to host management team
    def test_get_host_info_host_management_team(self):
        response = self.client.get("/api/host/", **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Access denied to director because he is not part of host management team
    def test_get_host_info_director(self):
        access_token = self.get_token(self.DIRECTOR_EMAIL, self.PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/host/", **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Access denied to member outside host management team
    def test_get_host_info_no_host_management_team(self):
        access_token = self.get_token(self.NO_HOST_MANAGEMENT_EMAIL, self.PASSWORD)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/host/", **bearer)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Should show all host companies ordered by company field in "Ascending" order
    def test_get_hosts_all_order_asc(self):
        response = self.client.get("/api/host/", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        self.assertEqual(responseLength, 5)
        for ix in range(1, responseLength):
            self.assertLessEqual(hosts[ix-1]['company'].lower(), hosts[ix]['company'].lower())

    # Ordering by company field in "Ascending" order
    def test_get_hosts_ordering_by_company_asc(self):
        response = self.client.get("/api/host/?ordering=company", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(hosts[ix-1]['company'].lower(), hosts[ix]['company'].lower())

    # Ordering by company field in "Descending" order
    def test_get_hosts_ordering_by_company_desc(self):
        response = self.client.get("/api/host/?ordering=-company", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        for ix in range(1, responseLength):
            self.assertLessEqual(hosts[ix]['company'].lower(), hosts[ix-1]['company'].lower())

    # Search with no match
    def test_get_hosts_search_no_match(self):
        response = self.client.get("/api/host/?search=not_matching_anything", **self.bearer)
        responseLength = len(response.data)
        self.assertEqual(responseLength, 0)

    # Search with match only on company name only
    def test_get_hosts_search_company_match(self):
        response = self.client.get("/api/host/?search=big", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        self.assertEqual(responseLength, 1)
        self.assertEqual(hosts[0]['company'], "Big Panda")

    # Search with match on contact name only
    def test_get_hosts_search_contact_name_match(self):
        response = self.client.get("/api/host/?search=emm", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        self.assertEqual(responseLength, 1)
        self.assertEqual(hosts[0]['company'], "Big Panda")

    # Search with match on contact email only
    def test_get_hosts_search_contact_email_match(self):
        response = self.client.get("/api/host/?search=dav", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        self.assertEqual(responseLength, 1)
        self.assertEqual(hosts[0]['company'], "cisco")

    # Search with match on company name, contact name and contact email
    def test_get_hosts_search_match_all_search_fields(self):
        response = self.client.get("/api/host/?search=ad", **self.bearer)
        responseLength = len(response.data)
        hosts = json.loads(response.content)
        self.assertEqual(responseLength, 3)
        expected_companies = set(['Adobe', 'cisco', 'Big Panda'])
        name_of_companies = set()
        for host in hosts:
            name_of_companies.add(host['company'])
        self.assertSetEqual(expected_companies, name_of_companies)

    # Test create company without contacts
    def test_create_company_no_contacts(self):
        json_type = "application/json"
        data = json.dumps({"company": "no contacts",
                           "city": "somewhere",
                           "contacts": [],
                           "notes": "post test no contacts",
                           })
        response = self.client.post("/api/host/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        host_created = Host.objects.last()
        contacts_created = Contact.objects.filter(company_id=host_created.id)
        contactsLength = len(contacts_created)
        self.assertEqual(host_created.company, "no contacts")
        self.assertEqual(host_created.city, "somewhere")
        self.assertEqual(host_created.notes, "post test no contacts")
        self.assertEqual(host_created.created_by, host_created.updated_by)
        self.assertEqual(contactsLength, 0)

    # Test create company with valid contacts
    def test_create_company_with_valid_contacts(self):
        json_type = "application/json"
        data = json.dumps({"company": "contacts",
                           "city": "somewhere",
                           "contacts": [{
                               "name": "Elena",
                               "email": "elena@prueba.com",
                               "info": "main contact",
                               },
                                {
                               "name": "Morado",
                               "email": "morado@prueba.com",
                               "info": "second contact",
                               },
                                ],
                           "notes": "post test with contacts",
                           })
        response = self.client.post("/api/host/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        host_created = Host.objects.last()
        contacts_created = Contact.objects.filter(company_id=host_created.id)
        contactsLength = len(contacts_created)
        self.assertEqual(host_created.company, "contacts")
        self.assertEqual(host_created.city, "somewhere")
        self.assertEqual(host_created.notes, "post test with contacts")
        self.assertEqual(contactsLength, 2)

        contact_data = Contact.objects.get(id=contacts_created[0].id)
        self.assertEqual(contact_data.name, "Elena")
        self.assertEqual(contact_data.email, "elena@prueba.com")
        self.assertEqual(contact_data.info, "main contact")

        contact_data = Contact.objects.get(id=contacts_created[1].id)
        self.assertEqual(contact_data.name, "Morado")
        self.assertEqual(contact_data.email, "morado@prueba.com")
        self.assertEqual(contact_data.info, "second contact")

    # Test create company with invalid contacts
    def test_create_company_with_invalid_contacts(self):
        json_type = "application/json"
        long_name = 'a'*51
        data = json.dumps(
            {
                "company": "some_company",
                "city": "",
                "contacts": [
                    {
                        "name": long_name,
                        "email": "",
                        "info": "",
                    }
                ],
                "notes": "",
            }
        )
        response = self.client.post("/api/host/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test update company to remove contacts
    def test_update_company_no_contacts(self):
        json_type = "application/json"
        data = json.dumps({"id": 1,
                           "company": "update no contacts",
                           "city": "somewhere",
                           "contacts": [],
                           "notes": "update test no contacts",
                           })
        response = self.client.put("/api/host/1/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        host = Host.objects.get(id=1)
        contacts = Contact.objects.filter(company_id=1)
        contactsLength = len(contacts)
        self.assertEqual(host.company, "update no contacts")
        self.assertEqual(host.city, "somewhere")
        self.assertEqual(host.notes, "update test no contacts")
        self.assertEqual(contactsLength, 0)

    # Test update company to add valid contacts
    def test_update_company_add_valid_contacts(self):
        json_type = "application/json"
        data = json.dumps({"id": 4,
                           "company": "update add contacts",
                           "city": "somewhere",
                           "contacts": [{
                               "name": "Elena",
                               "email": "elena@prueba.com",
                               "info": "main contact",
                               },
                                {
                               "name": "Morado",
                               "email": "morado@prueba.com",
                               "info": "second contact",
                               }, ],
                           "notes": "update test add contacts",
                           })
        response = self.client.put("/api/host/4/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        host = Host.objects.get(id=4)
        contacts = Contact.objects.filter(company_id=4)
        contactsLength = len(contacts)
        self.assertEqual(host.company, "update add contacts")
        self.assertEqual(host.city, "somewhere")
        self.assertEqual(host.notes, "update test add contacts")
        self.assertEqual(contactsLength, 2)

        contact_data = Contact.objects.get(id=contacts[0].id)
        self.assertEqual(contact_data.name, "Elena")
        self.assertEqual(contact_data.email, "elena@prueba.com")
        self.assertEqual(contact_data.info, "main contact")

        contact_data = Contact.objects.get(id=contacts[1].id)
        self.assertEqual(contact_data.name, "Morado")
        self.assertEqual(contact_data.email, "morado@prueba.com")
        self.assertEqual(contact_data.info, "second contact")

    # Test update company add invalid contacts
    def test_update_company_add_invalid_contacts(self):
        json_type = "application/json"
        long_name = 'a'*51
        data = json.dumps(
            {
                "id": 4,
                "company": "some_company",
                "city": "",
                "contacts": [
                    {
                        "name": long_name,
                        "email": "",
                        "info": "",
                    }
                ],
                "notes": "",
            }
        )
        response = self.client.put("/api/host/4/", data, **self.bearer, accept=json_type, content_type=json_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that existing company is deleted
    def test_delete_valid_company(self):
        response = self.client.delete("/api/host/4/", **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test that nonexisting company can't be deleted
    def test_invalid_company_not_deleted(self):
        response = self.client.delete("/api/host/100/", **self.bearer)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

