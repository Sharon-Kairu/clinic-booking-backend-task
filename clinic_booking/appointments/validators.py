from django.utils import timezone 
from rest_framework.exceptions import ValidationError
from datetime import datetime,timedelta

from .models import Appointment

def not_past(date,start_time):
    appointment=datetime.combine(date,start_time)

    if timezone.make_aware(appointment)<timezone.now():
        raise ValidationError("Appoointments cannot be booked for the past")

def not_within_hour(date, start_time):
    appointment=datetime.combine(date,start_time)

    if(timezone.make_aware(appointment)<timezone.now()+ timedelta(hours=1)):
        raise ValidationError("Appointments must be booked at least one hour before the selecetd time")

def validate_working_hours(doctor,start_time):
    if(start_time<doctor.start_time or start_time>=doctor.end_time):
        raise ValidationError("The selected time is outside the doctor's set working hours")

def validate_booked_slots(date,doctor,start_time):
    booked=Appointment.objects.filter(doctor=doctor,date=date,start_time=start_time,status="Booked").exists()

    if booked:
        raise ValidationError('The slot is already booked')

def validate_cancelled(appointment):
    if appointment.status=="Cancelled":
        raise ValidationError("This appointment was cancelled")