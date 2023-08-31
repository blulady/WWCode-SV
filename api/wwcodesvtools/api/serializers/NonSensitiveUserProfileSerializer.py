from rest_framework import serializers
from django.contrib.auth.models import User
from api.serializers.NonSensitiveMemberInfoSerializer import NonSensitiveMemberInfoSerializer


class NonSensitiveUserProfileSerializer(NonSensitiveMemberInfoSerializer):
    city = serializers.CharField(source='userprofile.city', allow_blank=True, allow_null=True)
    state = serializers.CharField(source='userprofile.state', allow_blank=True, allow_null=True)
    country = serializers.CharField(source='userprofile.country', allow_blank=True, allow_null=True)
    timezone = serializers.CharField(source='userprofile.timezone', allow_blank=True, allow_null=True)
    bio = serializers.CharField(source='userprofile.bio', allow_blank=True, allow_null=True)
    photo = serializers.ImageField(source='userprofile.photo', max_length=None, allow_empty_file=False, allow_null=True, required=False)
    slack_handle = serializers.CharField(source='userprofile.slack_handle', allow_blank=True, allow_null=True)
    linkedin = serializers.CharField(source='userprofile.linkedin', allow_blank=True, allow_null=True)
    instagram = serializers.CharField(source='userprofile.instagram', allow_blank=True, allow_null=True)
    facebook = serializers.CharField(source='userprofile.facebook', allow_blank=True, allow_null=True)
    twitter = serializers.CharField(source='userprofile.twitter', allow_blank=True, allow_null=True)
    medium = serializers.CharField(source='userprofile.medium', allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'status', 'highest_role', 'date_joined', 'role_teams', 'city', 'state', 'country', 'timezone', 'bio', 'photo', 'slack_handle', 'linkedin', 'instagram', 'facebook', 'twitter', 'medium']
