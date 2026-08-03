from datetime import date, time, timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment


class AppointmentBookingTests(APITestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            firstname="James",
            lastname="Mwangi",
            specialization="Cardiology",
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        self.patient = Patient.objects.create(
            first_name="Alice", last_name="Wanjiru"
        )
       
        self.future_date = (timezone.localdate() + timedelta(days=5))

    def test_successful_booking(self):
        response = self.client.post("/appointments/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": self.future_date.isoformat(),
            "start_time": "10:00:00",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Booked")

    def test_double_booking_rejected(self):
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=self.future_date, start_time=time(10, 0), status="Booked"
        )
        response = self.client.post("/appointments/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": self.future_date.isoformat(),
            "start_time": "10:00:00",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_past_date_rejected(self):
        past_date = timezone.localdate() - timedelta(days=1)
        response = self.client.post("/appointments/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": past_date.isoformat(),
            "start_time": "10:00:00",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_within_one_hour_rejected(self):
        soon = timezone.now() + timedelta(minutes=20)
        response = self.client.post("/appointments/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": soon.date().isoformat(),
            "start_time": soon.time().strftime("%H:%M:%S"),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outside_working_hours_rejected(self):
        response = self.client.post("/appointments/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": self.future_date.isoformat(),
            "start_time": "18:00:00",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AppointmentCancelTests(APITestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            firstname="Grace", lastname="Otieno", specialization="Pediatrics",
            start_time=time(8, 0), end_time=time(16, 0),
        )
        self.patient = Patient.objects.create(first_name="Brian", last_name="Odhiambo")
        self.future_date = timezone.localdate() + timedelta(days=5)
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=self.future_date, start_time=time(9, 0), status="Booked"
        )

    def test_successful_cancel(self):
        response = self.client.patch(
            f"/appointments/{self.appointment.id}/cancel/",
            {"cancel_reason": "Patient unavailable"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Cancelled")
        self.assertEqual(self.appointment.cancel_reason, "Patient unavailable")

    def test_double_cancel_rejected(self):
        self.appointment.status = "Cancelled"
        self.appointment.save()

        response = self.client.patch(
            f"/appointments/{self.appointment.id}/cancel/",
            {"cancel_reason": "Trying again"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancelled_slot_becomes_available(self):
        self.client.patch(
            f"/appointments/{self.appointment.id}/cancel/",
            {"cancel_reason": "Patient unavailable"},
            format="json",
        )
        response = self.client.get(
            f"/doctors/{self.doctor.id}/availability/?date={self.future_date.isoformat()}"
        )
        self.assertIn("09:00", response.data["available_slots"])


class AppointmentRescheduleTests(APITestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            firstname="Peter", lastname="Kamau", specialization="Dermatology",
            start_time=time(10, 0), end_time=time(18, 0),
        )
        self.patient = Patient.objects.create(first_name="Cynthia", last_name="Njeri")
        self.future_date = timezone.localdate() + timedelta(days=5)
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=self.future_date, start_time=time(11, 0), status="Booked"
        )

    def test_successful_reschedule(self):
        new_date = self.future_date + timedelta(days=1)
        response = self.client.patch(
            f"/appointments/{self.appointment.id}/reschedule/",
            {"date": new_date.isoformat(), "start_time": "14:00:00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.date, new_date)
        self.assertEqual(self.appointment.start_time.strftime("%H:%M:%S"), "14:00:00")

    def test_old_slot_freed_after_reschedule(self):
        new_date = self.future_date + timedelta(days=1)
        self.client.patch(
            f"/appointments/{self.appointment.id}/reschedule/",
            {"date": new_date.isoformat(), "start_time": "14:00:00"},
            format="json",
        )
        response = self.client.get(
            f"/doctors/{self.doctor.id}/availability/?date={self.future_date.isoformat()}"
        )
        self.assertIn("11:00", response.data["available_slots"])

    def test_reschedule_into_taken_slot_rejected(self):
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=self.future_date, start_time=time(12, 0), status="Booked"
        )
        response = self.client.patch(
            f"/appointments/{self.appointment.id}/reschedule/",
            {"date": self.future_date.isoformat(), "start_time": "12:00:00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reschedule_cancelled_appointment_rejected(self):
        self.appointment.status = "Cancelled"
        self.appointment.save()
        new_date = self.future_date + timedelta(days=1)
        response = self.client.patch(
            f"/appointments/{self.appointment.id}/reschedule/",
            {"date": new_date.isoformat(), "start_time": "14:00:00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)