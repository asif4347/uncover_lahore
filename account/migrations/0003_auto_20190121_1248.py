# Generated by Django 2.1.5 on 2019-01-21 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190121_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='verification_code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
