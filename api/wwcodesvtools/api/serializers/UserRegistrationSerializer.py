from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..validators.FirstAndLastNameValidator import validate_first_name, validate_last_name
from ..validators.password_validator import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False, validators=[validate_first_name])
    last_name = serializers.CharField(write_only=True, validators=[validate_last_name])
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data['email']
        username = data['username']
        if (email is not None and username is not None and email != username):
            raise serializers.ValidationError({"email_username":
                                               "Email and Username should be same"})
        return data
