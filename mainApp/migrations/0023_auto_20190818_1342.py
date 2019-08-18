# Generated by Django 2.2.4 on 2019-08-18 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0022_auto_20190312_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Cultural', 'Cultural')], default='Adventure', max_length=30),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='mainApp.Activity'),
        ),
        migrations.AlterField(
            model_name='userschedule',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]