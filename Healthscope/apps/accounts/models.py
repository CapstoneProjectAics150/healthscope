from django.contrib.auth.models import User
from django.db import models

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    dob = models.DateField(null=True, blank=True)   # ✅ FIX

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)

    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)

    blood_group = models.CharField(max_length=5, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)