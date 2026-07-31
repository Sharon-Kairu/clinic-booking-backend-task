from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS=[
        ('Booked','booked'),
        ('Cancelled','cancelled')
    ]
    patient=models.ForeignKey(Patient, related_name='Patient-Appointment')
    doctor=models.ForeignKey(Doctor, related_name='Doctor-apointment')
    date=models.DateField()
    start_time=models.DateField
    status=models.CharField(choices=STATUS, default='Booked')
    cancel_reason=models.TextField()
    created_at=models.DateTimeField(auto_now=True)


