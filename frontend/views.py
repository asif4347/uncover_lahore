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
    return render(request, 'index.html', context)


def activities(request, pk):
    spot = Spot.objects.get(pk=pk)
    acts = Spot.activities.all()
    context = {
        'spot': spot,
        'activities': acts
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'account/login.html')


def register(request):
    return render(request, 'account/register.html')


def contact(request):
    return render(request, 'account/contact.html')

def spot(request):
    return render(request, 'spot.html')

def activities(request):
    return render(request, 'activities.html')
