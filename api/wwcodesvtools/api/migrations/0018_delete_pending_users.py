# Generated by Django 3.1 on 2023-06-08 21:37

from django.db import migrations


def delete_pending_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model("api", "UserProfile")
    User_Team = apps.get_model("api", "User_Team")

    userprofile_pending = UserProfile.objects.filter(status="PENDING")

    for people in userprofile_pending:
        user = User.objects.get(id=people.user.id)
        if user:
            user.delete()
        teams = User_Team.objects.filter(user=people.user.id)
        if teams:
            teams.delete()  # can this be a list comp?

    userprofile_pending.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20230528_2326'),
    ]

    operations = [
        migrations.RunPython(delete_pending_users),
    ]