from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------------- HOME ----------------
    path('', views.Home.as_view(), name="home"),

    # ---------------- AUTH ----------------
    path('signup/', views.Signup.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),

    # ---------------- ADMIN ----------------
    path('admin-home/', views.Admin_home.as_view(), name="admin-home"),
    path('admin-department/', views.Department.as_view(), name="admin-department"),
    path('add-doctor-admin/<int:i>/', views.Add_doctor.as_view(), name="add-doctor-admin"),
    path('edit-department-admin/<int:i>/', views.Edit_department_admin.as_view(), name="department-edit-admin"),
    path('edit-doctor-admin/<int:i>/', views.Edit_doctor_admin.as_view(), name="doctor-edit-admin"),
    path('remove-doctor/<int:i>/', views.Remove_doctor.as_view(), name="remove-doctor"),

    # Appointment management
    path('admin-appointment-list/', views.Admin_appointment_list.as_view(), name="admin-appointment-list"),
    path('approve-appointment/<int:i>/', views.Approve_appointment.as_view(), name="approve-appointment"),
    path('reject-appointment/<int:i>/', views.Reject_appointment.as_view(), name="reject-appointment"),

   
    # ---------------- PATIENT ----------------
path('patient-home/', views.Patient_home.as_view(), name="patient-home"),
path('doctor-view-patient/<int:i>/', views.Doctor_view_patient.as_view(), name="doctor-view-patient"),

# ✅ add a default (no-arg) route that your view already handles
path('add-patient/', views.Add_patient.as_view(), name="add-patient-default"),

# keep the existing one with department id
path('add-patient/<int:i>/', views.Add_patient.as_view(), name="add-patient"),

path('book-appointment/<int:i>/', views.Book_appointment.as_view(), name="book-appointment"),
path('patient-appointments/', views.Patient_appointment_list.as_view(), name="patient-appointments"),

]
