# Generated by Django 2.1.5 on 2019-02-06 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_perlsperusd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Cultural', 'Cultural')], default='Adventure', max_length=30),
        ),
    ]
