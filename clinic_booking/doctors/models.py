from django.db import models

class Doctor(models.Model):
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    specialization=models.CharField(max_length=50)
    start_time=models.TimeField()
    end_time=models.TimeField()
