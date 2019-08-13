from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/categories/', get_categories),
    path('api/get-perl-rate/', get_perls_rate),
    path('api/get-nearby-activities/', nearby_activities),
    path('api/add-schedule/', add_schedule),
    path('api/add-spot-schedule/', add_schedule_spots),
    path('api/get-schedules/', get_schedules),
    path('api/get-bookings/', get_bookings),
    path('api/get-activities/', get_activities),
    path('api/book-now/', book_now),
    path('api/global-search/', search_global),
    path('api/delete-schedule/<int:pk>', delete_schedule),
    path('api/pay-now/<int:pk>', pay_now),
    path('api/book-activity/', book_activity),

]
