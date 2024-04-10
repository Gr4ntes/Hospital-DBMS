from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("departments/", views.departments, name="departments"),
    path("staff/", views.staff, name="staff"),
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="login"),
    path("patients/<int:user_id>/", views.patient_account, name="patient_account"),
    path("patients/<int:user_id>/visits/", views.patient_visits, name="patient_visits"),
    path("patients/<int:user_id>/appointment/", views.patient_appointment, name="patient_appointment"),
    path("patients/<int:user_id>/appointment/<int:appointment_id>/delete/", views.delete_appointment,
         name="delete_appointment"),
    path("patients/<int:user_id>/inpatient/<int:inpatient_id>/delete/", views.delete_inpatient,
         name="delete_inpatient"),
    path("doctor/<int:user_id>/", views.doctor_account, name="doctor_account"),
    path("doctor/<int:user_id>/new_record/", views.doctor_record, name="doctor_record"),
    path("doctor/<int:user_id>/records/", views.doctor_records, name="doctor_records"),
    path("doctor/<int:user_id>/inpatient/", views.doctor_inpatient, name="doctor_inpatient"),
    path("doctor/<int:user_id>/new_inpatient/", views.doctor_new_inpatient, name="doctor_new_inpatient"),
    path("doctor/<int:user_id>/records/<int:appointment_id>/", views.record, name="record"),
    path('logout/', views.user_logout, name='logout'),
]
