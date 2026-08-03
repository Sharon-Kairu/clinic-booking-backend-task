# appointments/management/commands/seed_data.py
from datetime import time
from django.core.management.base import BaseCommand
from doctors.models import Doctor
from patients.models import Patient


class Command(BaseCommand):
    help = "Seed the database with 5 doctors and 5 patients"

    def handle(self, *args, **options):
        doctors_data = [
            {"firstname": "James", "lastname": "Mwangi", "specialization": "Cardiology", "start_time": time(9, 0), "end_time": time(17, 0)},
            {"firstname": "Grace", "lastname": "Otieno", "specialization": "Pediatrics", "start_time": time(8, 0), "end_time": time(16, 0)},
            {"firstname": "Peter", "lastname": "Kamau", "specialization": "Dermatology", "start_time": time(10, 0), "end_time": time(18, 0)},
            {"firstname": "Susan", "lastname": "Achieng", "specialization": "General Practice", "start_time": time(9, 0), "end_time": time(15, 0)},
            {"firstname": "David", "lastname": "Kiptoo", "specialization": "Orthopedics", "start_time": time(11, 0), "end_time": time(19, 0)},
        ]

        patients_data = [
            {"first_name": "Alice", "last_name": "Wanjiru"},
            {"first_name": "Brian", "last_name": "Odhiambo"},
            {"first_name": "Cynthia", "last_name": "Njeri"},
            {"first_name": "Dennis", "last_name": "Mutua"},
            {"first_name": "Esther", "last_name": "Chebet"},
        ]

        for d in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                firstname=d["firstname"], lastname=d["lastname"], defaults=d
            )
            self.stdout.write(f"{'Created' if created else 'Exists'}: Dr. {doctor.firstname} {doctor.lastname}")

        for p in patients_data:
            patient, created = Patient.objects.get_or_create(**p)
            self.stdout.write(f"{'Created' if created else 'Exists'}: {patient.first_name} {patient.last_name}")

        self.stdout.write(self.style.SUCCESS("Seeded 5 doctors and 5 patients"))