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


# Deployment & CI/CD

**Public URL:** https://clinic-booking-backend-task.onrender.com/


**Database:** MySQL, hosted on Aiven.

**Deploy branch:** main. Render's Auto-Deploy is enabled on main, so every
merge into main automatically triggers a new deployment —

**Pipeline description:**
On every pull request into the 'main' branch, a GitHub Actions workflow
(`.github/workflows/ci.yml`) checks the code, installs dependencies from
`requirements.txt`, and runs the Django test suite against a test database. 
If the tests pass and the PR is merged into main
Render detects the new commit and automatically rebuilds and redeploys the
application — reinstalling dependencies, running migrations, and restarting
the live service.


# AI Reflection

**1. What did I use AI for across the four sections?**
- Reviewing the assignment I needed to carry out and having a breakdown on tasks and checklist
- Writing a database seeder to populate the database with 5 patients and 5 doctors
- Debugging migration, database, and settings errors
- Reviewing errors I made in the imports and functions that had erros
- Structuring this README and identifying the sections required 

**2. Example where AI improved my work:**
I asked it to review my cancel_appointment function. It found that the
function overwrote the cancel reason with an empty string instead of saving
the value from the request, and that the function signature was passing
the wrong parameter. This would have silently discarded every cancellation
reason submitted by users.

**3. Example where AI output was wrong or incomplete:**
  In the logic of the appointments, the model I used for guidance did not cater for appointment dates. It only
  focused on time and this left a gap of the appointments being tied to only one day yet the patients should set the appointments
  to whatever date they'd have wanted

**4. Two decisions I made without AI:**
 (a) The structuring of the files and deciding to have the services and validation separate from views
 (b) The apps I was to have used-patient,doctor and appointments and the structure of thhe models