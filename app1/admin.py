from django.contrib import admin
from .models import Department_model,Add_doctor_model,Add_patient_model,Appointment_model

# Register your models here.
admin.site.register(Department_model)
admin.site.register(Add_doctor_model)
admin.site.register(Add_patient_model)
admin.site.register(Appointment_model)