from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS=[
        ('Booked','booked'),
        ('Cancelled','cancelled')
    ]
    patient=models.ForeignKey(Patient, related_name='PatientAppointment', on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, related_name='DoctorApointment',on_delete=models.CASCADE)
    date=models.DateField()
    start_time=models.TimeField()
    status=models.CharField(choices=STATUS, default='Booked',max_length=10)
    cancel_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


