from .serializers import *
from random import randint
from rest_framework_jwt.settings import api_settings

api_response = {}


def success_response(data, msg):
    api_response['success'] = True
    api_response['message'] = msg
    api_response['data'] = data
    return api_response


def failure_response(data, msg):
    api_response['success'] = False
    api_response['message'] = msg
    api_response['data'] = None
    return api_response


def random_with_n_digits():
    range_start = 10 ** (4 - 1)
    range_end = (10 ** 4) - 1
    return randint(range_start, range_end)


def get_errors(serializer):
    errors = dict()
    for error in serializer.errors:
        errors[error] = serializer.errors[error][0]
    return errors


def error(serializer):
    errors = []
    for error in serializer.errors:
        errors.append(str(serializer.errors[error][0]))
        # errors[i] = serializer.errors[error][0]
    return errors


def get_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def jwt_response_payload_handler(token, user=None, request=None):
    if user is not None:
        return success_response(data={
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }, msg='Successfully logged in')
    if user is None:
        return failure_response(data={}, msg='Invalid login details')
