from django.urls import path
from .views import DoctorListView, DoctorDetailView
from appointments.views import DoctorAvailabilityView

urlpatterns = [
    path("", DoctorListView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),
    path("<int:id>/availability/", DoctorAvailabilityView.as_view()),
]