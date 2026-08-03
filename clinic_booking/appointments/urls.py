from django.urls import path
from .views import BookAppointmentView, CancelAppointmentView, RescheduleAppointmentView

urlpatterns = [
    path("", BookAppointmentView.as_view()),
    path("<int:id>/cancel/", CancelAppointmentView.as_view()),
    path("<int:id>/reschedule/", RescheduleAppointmentView.as_view()),
]