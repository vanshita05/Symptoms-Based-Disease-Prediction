# Generated by Django 5.0.3 on 2024-05-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_chat_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
