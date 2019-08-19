from django.urls import path, include
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('', index, name='index'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('contact', contact, name='contact'),
    path('my-bookings', bookings, name='my-bookings'),
    path('payment/<int:pk>', payment, name='payment'),
    path('spot/<int:pk>', spots, name='spots'),
    path('activities/<int:pk>', activities, name='activities'),
    path('activity-detail/<int:pk>', activity_detail, name='activity-detail')
]
