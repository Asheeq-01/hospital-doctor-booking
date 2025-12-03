from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import (
    Signup_form, Login_form, Department_form,
    Add_doctor_form, Add_patient_form, Appointment_form
)
from .models import (
    Department_model, Add_doctor_model,
    Add_patient_model, Appointment_model
)


# -------------------- HOME --------------------
class Home(View):
    def get(self, request):
        return render(request, 'home.html')


# -------------------- AUTH --------------------
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html', {'form': Signup_form()})

    def post(self, request):
        form = Signup_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Please login.")
            return redirect('login')
        messages.error(request, "Signup failed. Please correct the errors.")
        return render(request, 'signup.html', {'form': form})


class Login(View):
    def get(self, request):
        return render(request, 'login.html', {'form': Login_form()})

    def post(self, request):
        form = Login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, "Login successful!")

                if user.is_superuser:
                    return redirect('admin-home')

                # normal user flow
                patient_profile = Add_patient_model.objects.filter(user=user).first()
                if patient_profile:
                    return redirect('patient-home')

                first_dept = Department_model.objects.first()
                if first_dept:
                    return redirect('add-patient', i=first_dept.id)
                messages.warning(request, "No departments found. Please contact admin.")
                return redirect('home')

            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the form errors.")
        return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect('login')


# -------------------- ADMIN VIEWS --------------------
@method_decorator(login_required, name='dispatch')
class Admin_home(View):
    def get(self, request):
        return render(request, 'admin1/home.html')


@method_decorator(login_required, name='dispatch')
class Department(View):
    def get(self, request):
        return render(request, 'admin1/department.html', {
            'form': Department_form(),
            'view': Department_model.objects.all()
        })

    def post(self, request):
        form = Department_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
        return redirect('admin-department')


@method_decorator(login_required, name='dispatch')
class Add_doctor(View):
    def get(self, request, i):
        department = get_object_or_404(Department_model, id=i)
        return render(request, 'admin1/add_doctor.html', {
            'department': department,
            'de': department.doctor.all(),
            'form': Add_doctor_form()
        })

    def post(self, request, i):
        department = get_object_or_404(Department_model, id=i)
        form = Add_doctor_form(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.department = department
            doctor.save()
            messages.success(request, "Doctor added successfully.")
        return redirect('add-doctor-admin', i=i)


@method_decorator(login_required, name='dispatch')
class Edit_department_admin(View):
    def get(self, request, i):
        dept = get_object_or_404(Department_model, id=i)
        return render(request, 'admin1/edit_department.html', {'edit': Department_form(instance=dept)})

    def post(self, request, i):
        dept = get_object_or_404(Department_model, id=i)
        form = Department_form(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
        return redirect('admin-department')


@method_decorator(login_required, name='dispatch')
class Edit_doctor_admin(View):
    def get(self, request, i):
        doctor = get_object_or_404(Add_doctor_model, id=i)
        return render(request, 'admin1/edit_doctor.html', {'edit': Add_doctor_form(instance=doctor)})

    def post(self, request, i):
        doctor = get_object_or_404(Add_doctor_model, id=i)
        form = Add_doctor_form(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor updated successfully.")
        return redirect('add-doctor-admin', i=doctor.department.id)


@method_decorator(login_required, name='dispatch')
class Remove_doctor(View):
    def get(self, request, i):
        doctor = get_object_or_404(Add_doctor_model, id=i)
        dept_id = doctor.department.id
        doctor.delete()
        messages.success(request, "Doctor removed successfully.")
        return redirect("add-doctor-admin", i=dept_id)


# -------------------- PATIENT SIDE --------------------
@method_decorator(login_required, name='dispatch')
class Patient_home(View):
    def get(self, request):
        if not Add_patient_model.objects.filter(user=request.user).exists():
            messages.warning(request, "Please complete your profile first.")
            first_dept = Department_model.objects.first()
            if first_dept:
                return redirect('add-patient', i=first_dept.id)
            messages.error(request, "No departments found. Please contact admin.")
            return redirect('home')

        departments = Department_model.objects.all()
        first_dept = Department_model.objects.first()
        return render(request, 'patient/home.html', {
            'department': departments,
            'first_dept': first_dept,
        })


@method_decorator(login_required, name='dispatch')
class Doctor_view_patient(View):
    def get(self, request, i):
        department = get_object_or_404(Department_model, id=i)
        doctors = Add_doctor_model.objects.filter(department=department)
        return render(request, 'patient/doctor_view.html', {
            'department': department,
            'doctors': doctors
        })


@method_decorator(login_required, name='dispatch')
class Add_patient(View):
    def get(self, request, i=None):
        if i is None:
            first_dept = Department_model.objects.first()
            if first_dept:
                return redirect('add-patient', i=first_dept.id)
            messages.error(request, "No departments found. Please contact admin.")
            return redirect('patient-home')

        department = get_object_or_404(Department_model, id=i)
        return render(request, 'patient/add_patient.html', {
            'form': Add_patient_form(),
            'department': department
        })

    def post(self, request, i=None):
        if i is None:
            first_dept = Department_model.objects.first()
            if first_dept:
                return redirect('add-patient', i=first_dept.id)
            messages.error(request, "No departments found. Please contact admin.")
            return redirect('patient-home')

        department = get_object_or_404(Department_model, id=i)
        form = Add_patient_form(request.POST)

        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.department = department
            patient.save()
            messages.success(request, f"Patient '{patient.name}' added successfully!")
            return redirect('patient-home')

        return render(request, 'patient/add_patient.html', {
            'form': form,
            'department': department
        })


# -------------------- APPOINTMENTS --------------------
@method_decorator(login_required, name='dispatch')
class Book_appointment(View):
    def get(self, request, i):
        doctor = get_object_or_404(Add_doctor_model, id=i)
        patients = Add_patient_model.objects.filter(user=request.user)
        if not patients.exists():
            messages.warning(request, "Please add at least one patient profile first.")
            return redirect('patient-home')

        form = Appointment_form(user=request.user)
        return render(request, 'patient/book_appointment.html', {
            'doctor': doctor,
            'form': form,
        })

    def post(self, request, i):
        doctor = get_object_or_404(Add_doctor_model, id=i)
        form = Appointment_form(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, f"Appointment booked with Dr. {doctor.name} successfully! Waiting for approval.")
            return redirect('patient-appointments')
        return render(request, 'patient/book_appointment.html', {'doctor': doctor, 'form': form})


# -------------------- ADMIN - MANAGE APPOINTMENTS --------------------
@method_decorator(login_required, name='dispatch')
class Admin_appointment_list(View):
    def get(self, request):
        appts = Appointment_model.objects.select_related('patient', 'doctor').order_by('-id')
        return render(request, 'admin1/appointment_list.html', {'appointments': appts})


@method_decorator(login_required, name='dispatch')
class Approve_appointment(View):
    def get(self, request, i):
        appt = get_object_or_404(Appointment_model, id=i)
        appt.status = 'approved'
        appt.save()
        messages.success(request, "Appointment approved successfully.")
        return redirect('admin-appointment-list')


@method_decorator(login_required, name='dispatch')
class Reject_appointment(View):
    def get(self, request, i):
        appt = get_object_or_404(Appointment_model, id=i)
        appt.status = 'rejected'
        appt.save()
        messages.success(request, "Appointment rejected.")
        return redirect('admin-appointment-list')


# -------------------- PATIENT VIEW - APPOINTMENT LIST --------------------
@method_decorator(login_required, name='dispatch')
class Patient_appointment_list(View):
    def get(self, request):
        # ✅ FIX: show all appointments for all patients of this user
        patient_ids = Add_patient_model.objects.filter(user=request.user).values_list('id', flat=True)
        if not patient_ids:
            messages.warning(request, "Please add at least one patient profile first.")
            return redirect('patient-home')

        appts = Appointment_model.objects.filter(patient_id__in=patient_ids).select_related('doctor', 'patient').order_by('-id')
        return render(request, 'patient/appointment_list.html', {'appointments': appts})
