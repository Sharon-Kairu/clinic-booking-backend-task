from rest_framework import serializers
from .models import Appointment


class CreateAppointmentSer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "date", "start_time"]

class CancelAppointmentSer(serializers.Serializer):
    cancel_reason = serializers.CharField(required=True)

class RescheduleAppointmentSer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()