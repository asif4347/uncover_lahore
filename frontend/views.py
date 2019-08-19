from django.shortcuts import render
from mainApp.models import *


# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'index.html', context)


def spots(request, pk):
    category = Category.objects.get(pk=pk)
    spots = category.spots.all()
    context = {
        'category': category,
        'spots': spots
    }
    return render(request, 'spot.html', context)


def activities(request, pk):
    spot = Spot.objects.get(pk=pk)
    acts = spot.activities.all()
    context = {
        'spot': spot,
        'activities': acts
    }
    return render(request, 'activities.html', context)


def activity_detail(request, pk):
    activity = Activity.objects.get(pk=pk)
    schedules = Schedule.objects.filter(activity=activity)
    context = {
        'activity': activity,
        'schedules': schedules
    }
    return render(request, 'activity_detail_page.html', context)


def login(request):
    return render(request, 'account/login.html')


def register(request):
    return render(request, 'account/register.html')


def contact(request):
    return render(request, 'account/contact.html')


def payment(request, pk):
    booking = Booking.objects.get(pk=pk)
    return render(request, 'payment.html', {'booking': booking})


def bookings(request):
    return render(request, 'bookings.html')
