from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from uncover_qatar import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, error_messages={'required': 'gender field is required'})
    phone = models.CharField(max_length=20, null=True, error_messages={'required': 'phone field is required'})
    image = models.ImageField(null=True, blank=True)
    perls = models.IntegerField(null=True, default=0, blank=True)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    verification_code = models.IntegerField(null=True, blank=True, default=0)
    social_user = models.BooleanField(default=False)

    @property
    def get_image_url(self):
        if self.image:
            return settings.MY_HOST + str(self.image.url)
        else:
            return ''

    def __str__(self):
        if self.user:
            return self.user.first_name + " " + self.user.last_name + " (" + self.user.username + ")"


#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class ContactRequest(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=False)
    preferred_time = models.DateTimeField(null=False)

    def __str__(self):
        return self.name + " -- " + str(self.preferred_time)
