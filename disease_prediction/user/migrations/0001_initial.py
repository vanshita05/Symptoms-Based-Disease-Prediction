# Generated by Django 5.0.4 on 2024-04-22 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_doctor', models.BooleanField(default=True)),
                ('user_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile_no', models.CharField(max_length=15)),
                ('img', models.FileField(upload_to='')),
                ('registration_no', models.CharField(max_length=20)),
                ('qualification', models.CharField(max_length=20)),
                ('specialization', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='madmin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_admin', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile_no', models.CharField(max_length=15)),
                ('img', models.FileField(upload_to='')),
                ('password', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_user', models.BooleanField(default=True)),
                ('user_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile_no', models.CharField(max_length=15)),
                ('img', models.FileField(upload_to='')),
                ('password', models.CharField(max_length=12)),
            ],
        ),
    ]
