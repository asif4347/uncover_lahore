from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from .models import *
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^(?:0|\+?92)(?:\d\s?){10,10}$", "There must be 10 digits in phone number after +92 "
                                                                  "(+923218337902)")


class ProfileSerializer(ModelSerializer):
    phone = serializers.CharField(required=True, error_messages={'required': 'phone field is required'}, max_length=15,
                                  min_length=10, validators=[phone_validator])
    is_verified = serializers.BooleanField(read_only=True)
    image = serializers.CharField(read_only=True, source='get_image_url')
    verification_code = serializers.IntegerField(read_only=True)
    gender = serializers.CharField(max_length=20, required=True,
                                   error_messages={'required': 'gender field is required'})

    class Meta:
        model = Profile
        fields = (
            'gender',
            'phone',
            'image',
            'perls',
            'is_verified',
            'verification_code',
            'social_user',
        )


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8,
                                     error_messages={'required': 'password field is required'})
    profile = ProfileSerializer(read_only=True)
    email = serializers.EmailField(required=True, error_messages={'required': 'email field is required'},
                                   source='username', validators=[
            UniqueValidator(queryset=User.objects.all(), message='A user with same email already exists')])
    first_name = serializers.CharField(max_length=50, required=True,
                                       error_messages={'required': 'first name field is required'})
    last_name = serializers.CharField(max_length=50, required=True,
                                      error_messages={'required': 'last name field is required'})

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'profile',

        )


class LoginSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={'required': 'password field is required'})
    email = serializers.EmailField(required=True, source='username',
                                   error_messages={'required': 'email field is required'})

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class VerificationSerializer(ModelSerializer):
    verification_code = serializers.IntegerField(write_only=True, required=True,
                                                 error_messages={'required': 'verification_code field is required'})
    email = serializers.EmailField(required=True, source='username',
                                   error_messages={'required': 'email field is required'})

    class Meta:
        model = User
        fields = (
            'email',
            'verification_code',
        )


class ForgotPasswordSerializer(ModelSerializer):
    email = serializers.EmailField(required=True, source='username',
                                   error_messages={'required': 'email field is required'})

    class Meta:
        model = User
        fields = (
            'email',

        )


class ForgotPasswordConfirmSerializer(ModelSerializer):
    verification_code = serializers.IntegerField(write_only=True, required=True,
                                                 error_messages={'required': 'verification_code field is required'})
    email = serializers.EmailField(required=True, source='username',
                                   error_messages={'required': 'email field is required'})
    new_password = serializers.CharField(required=True, min_length=8,
                                         error_messages={'required': 'new_password field is required'})

    class Meta:
        model = User
        fields = (
            'email',
            'verification_code',
            'new_password',
        )


class ChangePasswordSerializer(ModelSerializer):
    old_password = serializers.CharField(required=True, error_messages={'required': 'old_password field is required'})
    new_password = serializers.CharField(required=True, min_length=8,
                                         error_messages={'required': 'new_password field is required'})

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, max_length=15,
                                  min_length=10, validators=[phone_validator])
    gender = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'address',
            'phone',
            'gender',

        )


class SocialAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'email field is required'},
                                   source='username')
    first_name = serializers.CharField(max_length=50, required=True,
                                       error_messages={'required': 'first name field is required'})
    last_name = serializers.CharField(max_length=50, required=True,
                                      error_messages={'required': 'last name field is required'})

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'email field is required'})
    name = serializers.CharField(max_length=50, required=True,
                                 error_messages={'required': 'name field is required'})
    phone = serializers.CharField(required=True, error_messages={'required': 'phone field is required'}, max_length=20,
                                  min_length=10, validators=[phone_validator])
    preferred_time = serializers.DateTimeField(required=True, error_messages={'required': 'preferred_time field is required'})

    class Meta:
        model = ContactRequest
        fields = '__all__'
