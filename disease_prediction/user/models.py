from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from datetime import date
# Create your models here.

class Madmin(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_admin = models.BooleanField(default=True)

    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=15)
    img = models.FileField()

    @property
    def age(self):
        today = date.today()
        db = self.dob
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age


class Usermodel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_user = models.BooleanField(default=True)

    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=15)
    img = models.FileField()

    @property
    def age(self):
        today = date.today()
        db = self.dob
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age


class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_doctor = models.BooleanField(default=True)

    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=15)
    img = models.FileField()
    registration_no = models.CharField(max_length=20)
    qualification = models.CharField(max_length=20)
    specialization = models.CharField(max_length=30)
    rating = models.IntegerField(default=0)

    @property
    def age(self):
        today = date.today()
        db = self.dob
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age


class Feedback(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __unicode__(self):
        return self.feedback


class Diseasescan(models.Model):

    patient = models.ForeignKey(Usermodel, null=True, on_delete=models.SET_NULL)

    diseasename1 = models.CharField(max_length=200)
    diseasename2 = models.CharField(max_length=200)
    diseasename3 = models.CharField(max_length=200)
    diseasename4 = models.CharField(max_length=200)
    diseasename5 = models.CharField(max_length=200)
    no_of_symp = models.IntegerField()
    symptomsname = ArrayField(models.CharField(max_length=200))
    confidence1 = models.DecimalField(max_digits=5, decimal_places=2)
    confidence2 = models.DecimalField(max_digits=5, decimal_places=2)
    confidence3 = models.DecimalField(max_digits=5, decimal_places=2)
    confidence4 = models.DecimalField(max_digits=5, decimal_places=2)
    confidence5 = models.DecimalField(max_digits=5, decimal_places=2)
    consultdoctor = models.CharField(max_length = 200)


    # def __str__(self):
    #     return self.patient.Usermodel.name



class consultation(models.Model):
    patient = models.ForeignKey(Usermodel, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    diseaseinfo = models.OneToOneField(Diseasescan, null=True, on_delete=models.SET_NULL)
    consultation_date = models.DateField()
    status = models.CharField(max_length = 20)


# from django.utils import timezone
# import pytz
from django.utils import timezone
import pytz

# Get India timezone
india_timezone = pytz.timezone('Asia/Kolkata')

# Get current time in India timezone
current_time_in_india = timezone.now().astimezone(india_timezone)

class Chat(models.Model):
    created = models.DateTimeField(default=current_time_in_india)
    consultation_id = models.ForeignKey(consultation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

class rating_review(models.Model):
    patient = models.ForeignKey(Usermodel, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)

    rating = models.IntegerField(default=0)
    review = models.TextField(blank=True)

    def __unicode__(self):
        return self.message