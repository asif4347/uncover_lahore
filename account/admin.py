from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.register(Profile)
admin.site.register(ContactRequest)
# admin.site.unregister(User)
admin.site.unregister(Group)
# admin.site.unregister(Site)
