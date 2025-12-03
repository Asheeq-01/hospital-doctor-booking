from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department_model(models.Model):
    name = models.CharField("Add Department", max_length=50)

class Add_doctor_model(models.Model):
    department = models.ForeignKey(Department_model, on_delete=models.CASCADE, related_name='doctor')
    name = models.CharField("doctor name", max_length=50)
    age = models.IntegerField("doctor age")
    choice_field = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField("gender", max_length=10, choices=choice_field)  # ✅ add max_length

class Add_patient_model(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='patients'
    )
    name = models.CharField("Patient Name", max_length=50)
    age = models.IntegerField("Age")
    choice_field = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField("Gender", choices=choice_field)
    department = models.ForeignKey(
        Department_model,
        on_delete=models.CASCADE,
        related_name='patient'
    )

    def __str__(self):
        return f"{self.name} ({self.gender.title()}, {self.age} yrs)"

    
    


class Appointment_model(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    patient = models.ForeignKey(Add_patient_model, on_delete=models.CASCADE, related_name='appointments')
    doctor  = models.ForeignKey(Add_doctor_model, on_delete=models.CASCADE, related_name='appointments')

    # Auto assign current date & time on create
    date    = models.DateField(default=timezone.now)
    time    = models.TimeField(default=timezone.now)

    status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason  = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} ({self.status})"
