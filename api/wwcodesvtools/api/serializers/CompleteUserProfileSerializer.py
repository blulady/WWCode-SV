from django.contrib.auth.models import User
from django.db import transaction
from api.serializers.NonSensitiveUserProfileSerializer import NonSensitiveUserProfileSerializer
from ..validators.FirstAndLastNameValidator import validate_first_name, validate_last_name
from utils.EmailSendingFailedError import EmailSendingFailedError
from api.helper_functions import send_email_helper
from rest_framework import serializers
from api.helper_functions import delete_file_from_media
import logging

logger = logging.getLogger('django')


class CompleteUserProfileSerializer(NonSensitiveUserProfileSerializer):

    USER_FIELDS = ['first_name', 'last_name']
    USERPROFILE_FIELDS = ['city', 'state', 'country', 'timezone', 'bio', 'photo', 'slack_handle', 'linkedin', 'instagram', 'facebook', 'twitter', 'medium']

    first_name = serializers.CharField(validators=[validate_first_name])
    last_name = serializers.CharField(validators=[validate_last_name])

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'status', 'highest_role', 'date_joined', 'role_teams', 'city', 'state', 'country', 'timezone', 'bio', 'photo', 'slack_handle', 'linkedin', 'instagram', 'facebook', 'twitter', 'medium']

    extra_kwargs = {
                'email': {'read_only': True},
                'date_joined': {'read_only': True},
            }

    def update(self, instance, validated_data):
        user = instance
        profile = instance.userprofile
        userprofile_data = validated_data.pop('userprofile')
        email = user.email
        photo_before_update = profile.photo

        # set user data
        user.first_name = validated_data.get('first_name', instance.first_name)
        user.last_name = validated_data.get('last_name', instance.last_name)

        # set profile data
        for k, v in userprofile_data.items():
            setattr(profile, k, v)
        with transaction.atomic():
            user.save()
            profile.save()
            email_sent = send_email_helper(email, 'User Profile updated at WWCode-Silicon Valley', 'userprofile_update_email.html', {})
            if not email_sent:
                raise EmailSendingFailedError()
        photo_after_update = profile.photo
        if photo_before_update != photo_after_update and photo_before_update:
            try:
                delete_file_from_media(photo_before_update.name)
            except Exception as e:
                logger.error(f'CompleteUserProfileSerializer Update: error deleting previous image: {e}')
        return user
