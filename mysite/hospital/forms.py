from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Patient


class createUserForm(UserCreationForm):
    class meta:
        model = User
        fields = ['username', 'password1', 'password2']


class patientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'age', 'email']

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone_number": "Phone Number",
            "gender": "Gender",
            "age": "Age",
            "email": "Email",
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)