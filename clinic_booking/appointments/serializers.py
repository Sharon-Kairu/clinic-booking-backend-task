from rest_framework import serializers
from .models import Appointment
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer

class CreateAppointmentSer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "date", "start_time"]

class CancelAppointmentSer(serializers.Serializer):
    cancel_reason = serializers.CharField(required=True)

class RescheduleAppointmentSer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()

class AppointmentDetailSer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "patient", "doctor", "date", "start_time", "status", "cancel_reason", "created_at"]
