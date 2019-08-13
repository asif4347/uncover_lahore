from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from account.serializers import phone_validator
from .models import *
from django.core.validators import RegexValidator


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            '__all__'
        )


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = (
            '__all__'
        )


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            '__all__'
        )


class ActivitySerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    # schedules = serializers.RelatedField(many=True, read_only=True)
    location = LocationSerializer()

    # spot_id = serializers.IntegerField(source='get_parent_spot', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id',
            'title',
            'background_image',
            'date_time',
            'description',
            'experts',
            'remember',
            'extra',
            'price',
            'seats',
            'category',
            'location',
            'gallery',
            'schedules',

        )


class SpotSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)
    location = LocationSerializer()
    activities = ActivitySerializer(many=True)

    class Meta:
        model = Spot
        fields = (
            '__all__'
        )


class CategorySerializer(serializers.ModelSerializer):
    spots = SpotSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'image',
            'spots',
        )


class UserScheduleSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(required=True, error_messages={'required': 'date time field is required'})
    description = serializers.CharField(max_length=500, required=True,
                                        error_messages={'required': 'description field is required'})
    activity_id = serializers.IntegerField(required=True, write_only=True,
                                           error_messages={'required': 'activity id is required'})
    activity = ActivitySerializer(read_only=True)
    spot = SpotSerializer(read_only=True)

    class Meta:
        model = UserSchedule
        fields = (
            'id',
            'date_time',
            'description',
            'is_spot',
            'activity',
            'activity_id',
            'spot'
        )


class UserSpotScheduleSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(required=True, error_messages={'required': 'date time field is required'})
    description = serializers.CharField(max_length=500, required=True,
                                        error_messages={'required': 'description field is required'})
    spot_id = serializers.IntegerField(required=True, write_only=True,
                                       error_messages={'required': 'Spot id is required'})

    class Meta:
        model = UserSchedule
        fields = (
            'date_time',
            'description',
            'spot_id',
        )


class BookingSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    payment_done = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    activity_id = serializers.IntegerField(write_only=True, required=True,
                                           error_messages={'required': 'activity_id field is required'})
    schedule_id = serializers.IntegerField(write_only=True, required=True,
                                           error_messages={'required': 'schedule_id field is required'})
    schedule = ScheduleSerializer(read_only=True)
    perls = serializers.IntegerField(write_only=True, required=True,
                                     error_messages={'required': 'perls field is required'})
    seats = serializers.IntegerField(write_only=True, required=True,
                                     error_messages={'required': 'seats field is required'})
    phone = serializers.CharField(required=True, error_messages={'required': 'phone field is required'}, max_length=20,
                                  min_length=10, validators=[phone_validator])

    class Meta:
        model = Booking
        fields = (
            'id',
            'payment_done',
            'activity',
            'activity_id',
            'perls',
            'seats',
            'phone',
            'schedule',
            'schedule_id',
        )
