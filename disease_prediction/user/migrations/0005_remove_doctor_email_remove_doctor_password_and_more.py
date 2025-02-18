# Generated by Django 5.0.4 on 2024-04-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_users_usermodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='password',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='user_name',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='password',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='user_name',
        ),
        migrations.AddField(
            model_name='doctor',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
