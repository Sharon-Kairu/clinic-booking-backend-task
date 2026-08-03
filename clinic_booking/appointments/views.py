from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.utils import timezone

from .models import Appointment
from .serializers import (
    CreateAppointmentSer,
    CancelAppointmentSer,
    RescheduleAppointmentSer,
    AppointmentDetailSer,
)
from .validators import (
    not_past,
    not_within_hour,
    validate_working_hours,
    validate_booked_slots,
)
from .services import cancel_appointment, reschedule_appointment
from doctors.models import Doctor


class BookAppointmentView(APIView):
    def post(self, request):
        serializer = CreateAppointmentSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        doctor = data["doctor"]
        date = data["date"]
        start_time = data["start_time"]

        not_past(date, start_time)
        not_within_hour(date, start_time)
        validate_working_hours(doctor, start_time)
        validate_booked_slots(date, doctor, start_time)

        appointment = serializer.save(status="Booked")
        return Response(AppointmentDetailSer(appointment).data, status=status.HTTP_201_CREATED)


class DoctorAvailabilityView(APIView):
    def get(self, request, id):
        doctor = get_object_or_404(Doctor, pk=id)
        date_str = request.query_params.get("date")

        if not date_str:
            return Response({"error": "date query param is required (YYYY-MM-DD)"}, status=400)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

        booked = set(
            Appointment.objects.filter(doctor=doctor, date=date, status="Booked")
            .values_list("start_time", flat=True)
        )

        slots = []
        current = datetime.combine(date, doctor.start_time)
        end = datetime.combine(date, doctor.end_time)
        while current < end:
            if current.time() not in booked:
                slots.append(current.time().strftime("%H:%M"))
            current += timedelta(minutes=30)

        return Response({"doctor": doctor.id, "date": date_str, "available_slots": slots})


class CancelAppointmentView(APIView):
    def patch(self, request, id):
        serializer = CancelAppointmentSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = cancel_appointment(id, serializer.validated_data)
        return Response(AppointmentDetailSer(appointment).data)


class RescheduleAppointmentView(APIView):
    def patch(self, request, id):
        serializer = RescheduleAppointmentSer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = reschedule_appointment(id, serializer.validated_data)
        return Response(AppointmentDetailSer(appointment).data)


class PatientAppointmentsView(APIView):
    def get(self, request, id):
        today = timezone.localdate()
        appointments = (
            Appointment.objects.filter(patient_id=id, date__gte=today)
            .order_by("date", "start_time")
        )
        return Response(AppointmentDetailSer(appointments, many=True).data)