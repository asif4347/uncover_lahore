# Generated by Django 2.1.5 on 2019-02-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20190207_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(error_messages={'required': 'phone field is required'}, max_length=20)),
                ('preferred_time', models.DateTimeField()),
            ],
        ),
    ]
