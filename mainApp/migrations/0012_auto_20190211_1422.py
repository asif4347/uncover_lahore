# Generated by Django 2.1.5 on 2019-02-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_auto_20190207_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Cultural', 'Cultural')], default='Adventure', max_length=30),
        ),
    ]
