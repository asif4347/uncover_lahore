from django.urls import path, include
from .views import *
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('register/', register,name='api-register'),
    path('login/', login,name="api-login"),
    path('verify/', verify),
    path('change-password/', change_password),
    path('update-profile/', save_profile),
    path('upload-image/', image_save),
    path('forgot-password/', forgot_password),
    path('forgot-password-confirm/', forgot_password_confirm),
    path('index/', index),
    path('social-auth/', social_login),
    path('contact-us/', contact_us),
]
