# clinic-booking-backend-task

System Design

System Overview
This project implements a RESTful API for a clinic appointment booking system using Django REST Framework.

The system allows patients to view a doctor's available appointment slots, book appointments, cancel existing bookings, and reschedule appointments while ensuring that scheduling rules are consistently enforced.

The application is designed around a simple architecture suitable for a small clinic with five doctors but follows design principles that allow it to scale as additional doctors, patients, and appointment records are introduced

Models
1. Doctor

Represents a doctor available for appointments.

Fields
ID-Unique identifier
First Name-Doctor's first name
Last Name-Doctor's last name
Specialization-Doctor's area of specialization
Working Start Time-Beginning of the doctor's working day
Working End Time-End of the doctor's working day

Each doctor has fixed daily working hours. Available appointment slots are generated dynamically based on these working hours rather than being stored in the database.

2. Patient

Represents a patient who can book appointments.

Fields
ID-Unique identifier
First Name-Patient's first name
Last Name-Patient's last name

Patients can create multiple appointments with different doctors over time.

3. Appointment

Represents a booking between a patient and a doctor.

Fields	
ID-Unique identifier
Patient-Reference to the patient
Doctor-Reference to the doctor
Date-The date of the appointment
Start Time-Beginning of the appointment
Status	Current-appointment status either ooked or cancelled
Cancel Reason-Reason provided when cancelling an appointment. Remains empty if the appointment is not canceledd
Created At-Timestamp indicating when the appointment was created

Appointments are scheduled in fixed 30-minute intervals. An appointment can either be active (Booked) or Cancelled.


# System Components

The application is organized into several components, each with a single responsibility.

1. Models

Store and manage the application's data using Django ORM.

2. Serializers

Validate incoming request data, serialize model instances into JSON responses, and enforce API-level validation.

3. Views

Handle HTTP requests and responses while delegating business operations to dedicated service functions.

4. Services

Contain the application's business logic, including appointment booking, cancellation, rescheduling, and availability calculations. Separating this logic from the views improves readability and makes the code easier to test.

5. Validators

Encapsulate reusable validation rules such as:

Appointment must not be in the past.
Appointment must fall within the doctor's working hours.
Appointment slot must be available.
Cancelled appointments cannot be rescheduled.
An already cancelled appointment cannot be cancelled again.

Design Decisions
1. Dynamic slot generation

Rather than storing every possible appointment slot in the database, available slots are generated dynamically from each doctor's working hours.

This reduces unnecessary data storage and ensures that availability always reflects the current appointment schedule.

2. Appointment status instead of deletion

Cancelled appointments are retained by changing their status to Cancelled rather than deleting them.

This preserves historical appointment records while immediately making the cancelled time slot available for future bookings.

3. Separation of concerns

Business logic is separated from the API views into dedicated service functions.

This keeps the views lightweight, improves maintainability, and allows business rules to be tested independently.

4. Fixed appointment duration

Appointments are fixed at 30-minute intervals, matching the requirements provided in the assessment.

Using a fixed duration simplifies availability calculations and prevents overlapping appointments