# Generated by Django 3.2 on 2023-09-14 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_default_active_status_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RegistrationToken',
        ),
    ]
