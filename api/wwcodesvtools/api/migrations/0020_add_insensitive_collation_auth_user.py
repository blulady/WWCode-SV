# Generated by Django 3.2 on 2023-06-16 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_case_insensitive_collation'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE "auth_user" ALTER COLUMN "last_name" TYPE varchar(255) COLLATE "case_insensitive"'),
        migrations.RunSQL('ALTER TABLE "auth_user" ALTER COLUMN "first_name" TYPE varchar(255) COLLATE "case_insensitive"'),
    ]
