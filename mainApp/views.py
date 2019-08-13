import datetime

import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .models import *
from pprint import pprint
from multiprocessing import Process
from django.core.mail import send_mail
from uncover_qatar import settings
import jwt, json
from account.utils import *
from rest_framework_jwt.settings import api_settings
import json
import pytz

utc = pytz.UTC


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            success_response(data=serializer.data, msg='Successfully retrieved categories'),
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def add_schedule(request):
    user = request.user
    try:
        # activity = Activity.objects.get(pk=id)
        serializer = UserScheduleSerializer(data=request.data)
        if serializer.is_valid():
            id = int(request.data['activity_id'])
            schedule = serializer.save()
            activity = Activity.objects.get(pk=id)
            schedule.user = user
            schedule.activity = activity
            schedule.save()
            return Response(
                success_response(data=serializer.data, msg='Activity added to schedule'),
                status=status.HTTP_200_OK
            )
        else:
            errors = error(serializer)
            return Response(
                data=failure_response(data={}, msg=errors[0]),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
    except Activity.DoesNotExist:
        return Response(
            failure_response(data={}, msg='Activity with provided id does not exist'),
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def add_schedule_spots(request):
    user = request.user
    try:
        # activity = Activity.objects.get(pk=id)
        serializer = UserSpotScheduleSerializer(data=request.data)
        if serializer.is_valid():
            id = int(request.data['spot_id'])
            schedule = serializer.save()
            spot = Spot.objects.get(pk=id)
            schedule.user = user
            schedule.spot = spot
            schedule.is_spot = True
            schedule.save()
            return Response(
                success_response(data=UserScheduleSerializer(schedule).data, msg='Spot added to schedule'),
                status=status.HTTP_200_OK
            )
        else:
            errors = error(serializer)
            return Response(
                data=failure_response(data={}, msg=errors[0]),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
    except Activity.DoesNotExist:
        return Response(
            failure_response(data={}, msg='Spot with provided id does not exist'),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def get_schedules(request):
    user = request.user
    schedules = UserSchedule.objects.filter(user=user)

    if schedules.__len__() == 0:
        return Response(
            failure_response(data={}, msg='no data found'),
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            success_response(data=UserScheduleSerializer(schedules, many=True).data,
                             msg='Successfully retrieved schedules'),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def delete_schedule(request, pk):
    user = request.user
    try:
        schedule = UserSchedule.objects.get(pk=pk)
        if schedule.user == user:
            schedule.delete()
            return Response(
                success_response(data=None,
                                 msg='Successfully deleted schedule'),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                failure_response(data={},
                                 msg="You are not authorized to delete someone else's schedule"),
                status=status.HTTP_200_OK
            )
    except UserSchedule.DoesNotExist:
        return Response(
            failure_response(data={}, msg='Schedule with provided id does not exist'),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def get_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    if bookings.__len__() == 0:
        return Response(
            failure_response(data={}, msg='no data found'),
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            success_response(data=BookingSerializer(bookings, many=True).data,
                             msg='Successfully retrieved bookings'),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_activities(request):
    user = request.user
    activities = Activity.objects.all()
    if activities.__len__() == 0:
        return Response(
            failure_response(data={}, msg='no data found'),
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            success_response(data=ActivitySerializer(activities, many=True).data,
                             msg='Successfully retrieved Activities'),
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def book_now(request):
    user = request.user
    try:
        #
        activity_id = int(request.data['activity_id'])
        if activity_id > 0:
            activity = Activity.objects.get(pk=activity_id)
            booking = Booking.objects.create(user=user, activity=activity)
            return Response(
                success_response(data=BookingSerializer(booking).data,
                                 msg='Successfully Booked activity'),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                failure_response(data={}, msg='activity_id is required'),
                status=status.HTTP_200_OK
            )

    except Activity.DoesNotExist:
        return Response(
            failure_response(data={}, msg='Activity with provided id does not exist'),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def search_global(request):
    q = request.GET.get('query', '')
    activities = Activity.objects.filter(title__icontains=q) | \
                 Activity.objects.filter(location__title__icontains=q)
    categories = Category.objects.filter(title__icontains=q)
    spots = Spot.objects.filter(title__icontains=q) | Spot.objects.filter(location__title__icontains=q)
    data = dict()
    data['activities'] = ActivitySerializer(activities, many=True).data
    data['categories'] = CategorySerializer(categories, many=True).data
    data['spots'] = SpotSerializer(spots, many=True).data
    return Response(
        success_response(data=data,
                         msg="Retrieved Data"),
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_perls_rate(request):
    rates = PerlsPerQAR.objects.all()
    data = dict()
    if rates.__len__() > 0:
        data['perl_rate'] = rates.last().perl_rate
        return Response(
            success_response(data=data, msg='Successfully got perl rate'),
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            failure_response(data=None, msg="No Rate added yet"),
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def nearby_activities(request):
    lat = request.data.get('lat')
    long = request.data.get('long')
    if not lat or not long or lat.__len__() < 2 or long.__len__() < 2:
        return Response(
            failure_response(data=None, msg='unable to validate the location'), status=200
        )

    locations = Location.objects.all()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + lat + ',' + long + '&destinations='
    dest_lat_langs = ''
    for loc in locations:
        dest_lat_langs += str(loc.lat) + ',' + str(loc.long) + '|'
    key = settings.GOOGLE_MAP_API
    final_url = url + dest_lat_langs + key
    map_data = requests.get(final_url)
    # pprint(map_data)
    json_data = map_data.json()['rows'][0]['elements']
    # pprint(json_data)
    if json_data[0]['status'] == 'ZERO_RESULTS' or json_data[0]['status'] == 'NOT_FOUND':
        return Response(failure_response(data=None, msg='No nearby services'), status=status.HTTP_200_OK)
    location_index = 0
    near_locations = []
    for json_location in json_data:
        distance = json_location['distance']['value'] / 1000  # distance in KM
        # pprint(distance)
        if 0 <= distance <= 10:
            near_locations.append(location_index)
        location_index += 1
    # pprint(near_locations)
    nearby_services = []
    activities = Activity.objects.all()
    for loc in near_locations:
        # pprint(locations[loc])
        ser = activities.filter(location=locations[loc]).first()

        if ser:
            nearby_services.append(ser)

    if nearby_services.__len__() > 0:
        return Response(
            success_response(data=ActivitySerializer(nearby_services, many=True).data, msg="Nearby Activities"),
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            failure_response(data=None, msg="No Nearby Activities"),
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def book_activity(request):
    user = request.user
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        activity_id = request.data.get('activity_id', '')
        perls = int(request.data.get('perls'))
        seats = int(request.data.get('seats'))
        phone = request.data.get('phone')
        schedule_id = int(request.data.get('schedule_id'))
        try:
            activity = Activity.objects.get(pk=int(activity_id))
        except Activity.DoesNotExist:
            return Response(
                failure_response(data=None, msg="Activity does not exist with given id"),
                status=200
            )

        try:
            schedule = activity.schedules.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            return Response(
                failure_response(data=None, msg="Schedule does not belong to current activity"),
                status=200
            )
        if seats > schedule.seats:
            return Response(
                failure_response(data=None, msg="Activity with this schedule does not have enough seats"),
                status=200
            )
        if perls > user.profile.perls:
            return Response(
                failure_response(data=None, msg="You don't have enough perls"),
                status=200
            )
        if schedule.start_time.replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc):
            return Response(
                failure_response(data=None, msg="Activity Schedule time has passed"),
                status=200
            )

        user.profile.perls -= perls
        user.profile.save()
        perl_rate = PerlsPerQAR.objects.all().last().perl_rate
        total_price = float(seats * activity.price)
        activity.seats -= seats
        activity.save()
        if perls > 0 and perl_rate > 0:
            total_price = total_price - (perls / perl_rate)
        bookings = Booking.objects.filter(activity=activity, user=user, schedule_id=schedule_id)
        if bookings:
            return Response(
                failure_response(data=None, msg="You have already booked this schedule for this activity"),
                status=200
            )

        booking = Booking.objects.create(activity=activity, user=user, seats=seats, total_price=total_price,
                                         phone=phone, schedule=schedule)
        schedule.seats -= seats
        schedule.save()

        data = {

            "token": settings.PAYMENT_TOKEN,
            "currencyCode": "QAR",
            "orderId": booking.id,
            "Note": "payment for booking " + activity.title,
            "isRecurring": False,
            "customerEmail": user.email,
            "customerCountry": "QATAR",
            "Lang": "ar",
            "Amount": total_price,
        }
        json_data = json.dumps(data)

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",

        }
        url = "https://maktapp.credit/v2/AddTransaction"
        response = requests.request("POST", url, data=json_data
                                    , headers=headers)
        if response.status_code == 200:
            return Response(
                success_response(data=json.loads(response.text)['result'], msg='Follow the link to make payment'),
                status=200
            )

    errors = error(serializer)
    return Response(

        data=failure_response(data={}, msg=errors[0]),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )


def booking_success(request):
    pk = request.GET.get('orderId')
    transid = request.GET.get('transid')
    booking = Booking.objects.get(pk=pk)
    booking.payment_done = True
    booking.transaction_id = transid
    perl_rate = PerlsPerQAR.objects.all().last().perl_rate
    total_price = float(booking.seats * booking.total_price)
    perls = int(total_price / perl_rate)
    booking.user.profile.perls += perls
    booking.user.profile.save()
    booking.activity.save()
    print(pk,transid)
    booking.save()
    return HttpResponse('<h3>Booking Successful</h3>')


@api_view(['GET'])
def pay_now(request, pk):
    booking = Booking.objects.get(pk=pk)
    data = {
        "token": settings.PAYMENT_TOKEN,
        "currencyCode": "QAR",
        "orderId": booking.id,
        "Note": "payment for booking " + booking.activity.title,
        "isRecurring": False,
        "customerEmail": booking.user.email,
        "customerCountry": "QATAR",
        "Lang": "ar",
        "Amount": booking.total_price
    }
    json_data = json.dumps(data)
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",

    }
    url = "https://maktapp.credit/v2/AddTransaction"
    response = requests.request("POST", url, data=json_data
                                , headers=headers)

    if response.status_code == 200:
        return Response(
            success_response(data=json.loads(response.text)['result'], msg='Follow the link to make payment'),
            status=200
        )

    return Response(

        data=failure_response(data={}, msg="Error in paying"),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )
