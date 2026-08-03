# patients/urls.py
from django.urls import path
from .views import PatientListView, PatientDetailView
from appointments.views import PatientAppointmentsView

urlpatterns = [
    path("", PatientListView.as_view()),
    path("<int:pk>/", PatientDetailView.as_view()),
    path("<int:id>/appointments/", PatientAppointmentsView.as_view()),
]