# Generated by Django 5.0.3 on 2024-05-14 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_chat_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 11, 21, 36, 359248, tzinfo=datetime.timezone.utc)),
        ),
    ]
