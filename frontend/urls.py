from django.urls import path, include
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('', index, name='index'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('contact',contact, name='contact'),
    path('spot',spot, name='spot'),
    path('activities',activities, name='activities')
]
