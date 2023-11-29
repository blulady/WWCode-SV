# Generated by Django 3.1 on 2021-04-06 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_auto_20210302_0718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(through='api.User_Team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_team',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.role'),
        ),
        migrations.RemoveConstraint(
            model_name='user_team',
            name='unique user_team',
        ),
        migrations.AlterField(
            model_name='user_team',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.team'),
        ),
        migrations.AddConstraint(
            model_name='user_team',
            constraint=models.UniqueConstraint(fields=('user_id', 'team_id', 'role_id'), name='unique user_team'),
        ),
    ]
