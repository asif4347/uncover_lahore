# Generated by Django 2.1.5 on 2019-02-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_auto_20190206_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('Cultural', 'Cultural'), ('Adventure', 'Adventure')], default='Adventure', max_length=30),
        ),
    ]
