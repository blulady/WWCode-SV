from api.models import Mentor
from rest_framework import serializers
from django.db import transaction


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ('id', 'first_name', 'last_name', 'email', 'level', 'reliability', 'created_by', 'updated_by')

        extra_kwargs = {
            'created_by': {'write_only': True},
            'updated_by': {'write_only': True}
        }

        @transaction.atomic
        def create(self, validated_data):
            mentor = Mentor.objects.create(**validated_data)
            return mentor

        @transaction.atomic
        def update(self, instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.level = validated_data.get('level', instance.level)
            instance.updated_by = validated_data.get('updated_by', instance.updated_by)
            instance.save()
            return instance

