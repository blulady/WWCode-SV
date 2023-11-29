from api.models import Host, Contact
from rest_framework import serializers
from django.db import transaction


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, max_length=50)

    class Meta:
        model = Contact
        fields = ('name', 'email', 'info')


class HostSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Host
        fields = ('id', 'company', 'city', 'contacts', 'notes', 'created_by', 'updated_by')

        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        # Getting the contacts, now validated_data has only the company info
        contacts_data = validated_data.pop('contacts', [])
        # Creating the company
        company = Host.objects.create(**validated_data)

        # Creating each contact
        for contact in contacts_data:
            name = contact.get("name")
            email = contact.get("email")
            info = contact.get("info")
            # Only save non-empty contacts
            if name or email or info:
                Contact.objects.create(company=company, **contact)

        return company

    @transaction.atomic
    def update(self, instance, validated_data):
        # Get contacts
        contacts_data = validated_data.pop('contacts', [])

        # Update Host instance
        instance.company = validated_data.get('company', instance.company)
        instance.city = validated_data.get('city', instance.city)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()

        # Delete all contacts
        instance.contacts.all().delete()

        # Creating each contact
        for contact in contacts_data:
            name = contact.get("name")
            email = contact.get("email")
            info = contact.get("info")
            # Only save non-empty contacts
            if name or email or info:
                Contact.objects.create(company=instance, **contact)

        return instance
