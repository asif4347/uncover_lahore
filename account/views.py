from django.contrib.auth import authenticate
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
from .utils import *
from rest_framework_jwt.settings import api_settings


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    if request.method == 'POST':
        serialized_user = UserSerializer(data=request.data)
        serialized_profile = ProfileSerializer(data=request.data)
        if serialized_user.is_valid() and serialized_profile.is_valid():
            user = serialized_user.save()
            user.set_password(request.data['password'])
            user.email = user.username
            user.save()
            profile = serialized_profile.save()
            profile.user = user
            profile.verification_code = random_with_n_digits()
            profile.save()
            body = 'Your account for Uncover Lahore is ready. Kindly enter the verification code ' \
                   'below\nVerification Code: ' + str(profile.verification_code)
            p = Process(target=send_mail,
                        args=('Uncover Lahore Verification Code', body, settings.EMAIL_HOST_USER, [user.email]))
            p.start()
            return Response(data=success_response(data=serialized_user.data, msg="Account Created Successfully!"),
                            status=status.HTTP_201_CREATED)
        elif not serialized_profile.is_valid() or not serialized_user.is_valid():
            errors = error(serialized_user)
            profile_errors = error(serialized_profile)
            for err in profile_errors:
                errors.append(err)

            return Response(data=failure_response(data={}, msg=errors[0]),
                            status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    if request.method == 'POST':
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            errors = error(login_serializer)
            return Response(
                data=failure_response(data={}, msg=errors[0]),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(username=email, password=password)
        except User.DoesNotExist:
            return Response(data=failure_response(data={}, msg='Invalid email or password'),
                            status=status.HTTP_200_OK)
        if user:
            data = {
                'token': get_token(user),
                'user': UserSerializer(user, context={'request': request}).data
            }
            return Response(
                data=success_response(data=data, msg='Successfully logged in'),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )

        else:
            return Response(
                data=failure_response(data={}, msg='Invalid email or password'),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def verify(request):
    if request.method == 'POST':
        login_serializer = VerificationSerializer(data=request.data)
        if not login_serializer.is_valid():
            errors = error(login_serializer)
            return Response(

                data=failure_response(data={}, msg=errors[0]),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        email = request.data['email']
        verification_code = int(request.data['verification_code'])
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return Response(data=failure_response(data={}, msg='Invalid email'),
                            status=status.HTTP_200_OK)
        if user:
            if not user.profile.is_verified:
                if verification_code == user.profile.verification_code:
                    user.profile.verification_code = 0
                    user.profile.is_verified = True
                    user.profile.save()
                    data = {
                        'token': get_token(user),
                        'user': UserSerializer(user, context={'request': request}).data
                    }
                    return Response(
                        data=success_response(data=data, msg='Successfully Verified'),
                        status=status.HTTP_200_OK,
                        content_type="application/json"
                    )
                else:
                    return Response(
                        data=failure_response(data={}, msg='Invalid Code'),
                        status=status.HTTP_200_OK,
                        content_type="application/json"
                    )
            else:
                return Response(
                    data=failure_response(data={}, msg='User already verified'),
                    status=status.HTTP_200_OK,
                    content_type="application/json"
                )


@api_view(['POST'])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        errors = error(serializer)
        return Response(
            data=failure_response(data={}, msg=errors[0]),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    user = request.user
    if not user.check_password(serializer.data.get("old_password")):
        return Response(
            data=failure_response(data=get_errors(serializer), msg='Incorrect old password'),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    user.set_password(serializer.data.get("new_password"))
    user.save()
    return Response(
        data=success_response(data=UserSerializer(user).data, msg='Password successfully changed'),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = request.POST.get('email', '')
        user = User.objects.filter(username=email)
        if user:
            user = user.first()
            user.profile.verification_code = random_with_n_digits()
            user.profile.save()
            url = 'http://' + request.get_host() + '/api/forgot-password/?email=' + email + '&verification_code=' +str( user.profile.verification_code)
            body = 'Your account reset password for Uncover Lahore is here. Kindly enter the code ' \
                   'below\nReset Code: ' + str(user.profile.verification_code) + '\nor click ' + url + '\n' \
                                                                                                       'if you have not requested this, kindly ignore it'
            p = Process(target=send_mail,
                        args=('Uncover Lahore Password Reset Code', body, settings.EMAIL_HOST_USER, [user.email]))
            p.start()
            return Response(
                data=success_response(data=UserSerializer(user).data, msg='Password reset code sent'),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        else:
            return Response(
                data=failure_response(data={}, msg='Email does not belong to any account'),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
    errors = error(serializer)
    return Response(

        data=failure_response(data={}, msg=errors[0]),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def forgot_password_confirm(request):
    serializer = ForgotPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        email = request.POST.get('email', '')
        user = User.objects.filter(username=email)
        verification_code = int(request.POST.get('verification_code', ''))
        if user:
            user = user.first()
            if user.profile.verification_code == verification_code:
                user.profile.verification_code = 0
                user.set_password(request.POST.get('new_password', ''))
                user.profile.save()
                user.save()
                return Response(
                    data=success_response(data=UserSerializer(user).data, msg='Password reset successful'),
                    status=status.HTTP_200_OK,
                    content_type="application/json"
                )
            return Response(
                data=failure_response(data={}, msg='Invalid Code!'),
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        return Response(
            data=failure_response(data={}, msg='Email does not belong to any account'),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    errors = error(serializer)
    return Response(

        data=failure_response(data={}, msg=errors[0]),
        status=status.HTTP_200_OK,
        content_type="application/json"
    )


@api_view(['POST'])
def image_save(request):
    user = request.user
    data = dict()
    if request.method == 'POST':
        # print(request.FILES)
        image = request.FILES['image']
        try:
            person = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            person = Profile()
            person.user = user
        person.image = image
        person.save()
        data['image'] = str(person.image.url)
    return Response(data=success_response(data=data, msg='image uploaded successfully'), status=200)


@api_view(['POST'])
def save_profile(request):
    person = request.user.profile
    person.save()
    if request.method == 'POST':
        serializer = ProfileUpdateSerializer(data=request.data, instance=person)
        if serializer.is_valid():
            serializer.save()
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            password = request.POST.get('password', '')
            if first_name.__len__() > 0:
                person.user.first_name = first_name
            if last_name.__len__() > 0:
                person.user.last_name = last_name
            if password.__len__() > 0:
                if password.__len__() >= 8:
                    person.user.set_password(password)
                else:
                    return Response(failure_response(data={}, msg='Password must be at least 8 chars long'), status=200)
            person.user.save()
            person.save()
            return Response(success_response(data=UserSerializer(person.user).data, msg="profile updated successfully"),
                            status=200)
        else:
            errors = error(serializer)
            err = get_errors(serializer)
            # print(err)
            return Response(failure_response(data={}, msg=errors[0]),
                            status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def social_login(request):
    serializer = SocialAuthSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data['email']
        user = User.objects.filter(username=email).first()
        if not user:
            user = serializer.save()
            profile = Profile.objects.create(is_verified=True, social_user=True, user=user)
            user.profile = profile
            user.save()
        if not user.profile.is_verified:
            user.profile.is_verified = True
            user.profile.verification_code = 0
            user.profile.save()

        data = {
            'token': get_token(user),
            'user': UserSerializer(user, context={'request': request}).data
        }
        return Response(
            data=success_response(data=data, msg='Successfully logged in'),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    else:
        errors = error(serializer)
        return Response(
            data=failure_response(data={}, msg=errors[0]),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )


@api_view(['GET'])
def index(request):
    return Response({
        "Success"
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_us(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        req = serializer.save()
        return Response(
            data=success_response(data=ContactSerializer(req).data, msg='Successfully submitted contact request'),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )

    else:
        errors = error(serializer)
        return Response(
            data=failure_response(data={}, msg=errors[0]),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
