from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages


# Create your models here.


class Location(models.Model):
    lat = models.FloatField(null=False)
    long = models.FloatField(null=False)
    title = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(null=False)

    def __str__(self):
        return self.image.url


activity_actegories = {
    ('Cultural', 'Cultural'),
    ('Adventure', 'Adventure')
}


class Activity(models.Model):
    title = models.CharField(max_length=60, null=False)
    background_image = models.ImageField(null=False)
    date_time = models.DateTimeField(null=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    experts = models.TextField(max_length=500, null=True, blank=True)
    remember = models.TextField(max_length=500, null=True, blank=True)
    extra = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, null=False)
    seats = models.IntegerField(default=0, null=False)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    gallery = models.ManyToManyField(Gallery)
    category = models.CharField(null=False, max_length=30, choices=activity_actegories, default='Adventure')

    def __str__(self):
        return self.title

    @property
    def get_parent_spot(self):
        try:
            return self.spot_set().first().id
        except:
            return None


class Schedule(models.Model):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    seats = models.IntegerField(null=False)
    activity = models.ForeignKey(Activity, null=False, on_delete=models.CASCADE, related_name='schedules')

    class Meta:
        unique_together = ('activity', 'id')

    def __str__(self):
        return 'Start: ' + str(self.start_time) + ' Activity: ' + str(self.activity.title) + ' Seats: ' + str(
            self.seats)


class Spot(models.Model):
    title = models.CharField(max_length=60, null=False)
    background_image = models.ImageField(null=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    experts = models.TextField(max_length=500, null=True, blank=True)
    remember = models.TextField(max_length=500, null=True, blank=True)
    extra = models.TextField(max_length=500, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    gallery = models.ManyToManyField(Gallery)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50, null=False)
    image = models.ImageField(null=False)
    spots = models.ManyToManyField(Spot)

    def __str__(self):
        return self.title


class UserSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(null=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, null=True)
    is_spot = models.BooleanField(null=False, default=False)

    # def __str__(self):
    #     try:
    #         return self.activity
    #     except:
    #         return self.spot


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    payment_done = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, null=True)
    seats = models.IntegerField(null=False, default=0)
    total_price = models.FloatField(null=False, default=0.0)
    phone = models.CharField(max_length=15, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.activity.title


class PerlsPerQAR(models.Model):
    perl_rate = models.IntegerField(null=False, default=0)

    def save(self, *args, **kwargs):
        if PerlsPerQAR.objects.exists() and not self.pk:
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            # raise ValidationError('There is can be only one PersPerUsd instance, Please edit the one that exists')
            return ''
        return super(PerlsPerQAR, self).save(*args, **kwargs)

    def __str__(self):
        return "Perls Rate Per QAR: " + str(self.perl_rate)
