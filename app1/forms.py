from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Department_model,Add_doctor_model,Add_patient_model,Appointment_model


class Signup_form(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
        
class Login_form(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'enter username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password'}))
    
    
class Department_form(forms.ModelForm):
    class Meta:
        model=Department_model
        fields=['name']
        
        
class Add_doctor_form(forms.ModelForm):
    class Meta:
        model=Add_doctor_model
        fields=['name','age','gender']

class Add_patient_form(forms.ModelForm):
    class Meta:
        model=Add_patient_model
        fields=['name','age','gender']
        
        


class Appointment_form(forms.ModelForm):
    class Meta:
        model = Appointment_model
        fields = ['patient', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional note for the doctor...'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Add_patient_model.objects.filter(user=user)



        