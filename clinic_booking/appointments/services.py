from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Appointment
from .validators import (
    not_past,
    not_within_hour,
    validate_working_hours,
    validate_booked_slots,
    validate_cancelled,
)

def book_appointment(validated_data):
    doctor = validated_data["doctor"]
    patient = validated_data["patient"]
    date = validated_data["date"]
    start_time = validated_data["start_time"]

    not_past(date, start_time)
    not_within_hour(date,start_time)
    validate_working_hours(doctor,start_time)
    validate_booked_slots(doctor,date,start_time)

    Appointment.objects.create(doctor,patient,date,start_time)
    return Appointment

def cancel_appointment(id, validated_data):
    appointment = get_object_or_404(Appointment, pk=id)

    validate_cancelled(appointment) 
    appointment.status = "Cancelled"
    appointment.cancel_reason = validated_data.get("cancel_reason", "")
    appointment.save()
    return appointment


def reschedule_appointment(id, validated_data):
    appointment = get_object_or_404(Appointment, pk=id)

    validate_cancelled(appointment)

    date = validated_data["date"]
    start_time = validated_data["start_time"]
    doctor = appointment.doctor

    not_past(date, start_time)
    not_within_hour(date, start_time)
    validate_working_hours(doctor, start_time)

    slot_taken = (
        Appointment.objects.filter(
            doctor=doctor, date=date, start_time=start_time, status="Booked"
        )
        .exclude(pk=appointment.pk)
        .exists()
    )
    if slot_taken:
        raise ValidationError("The slot is already booked")

    appointment.date = date
    appointment.start_time = start_time
    appointment.save()
    return appointment
