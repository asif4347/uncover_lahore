# Generated by Django 2.1.5 on 2019-03-06 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_contactrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
