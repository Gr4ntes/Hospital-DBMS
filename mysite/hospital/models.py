from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    free_beds = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
    department = models.ForeignKey(Department, on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.IntegerField(validators=[MinValueValidator(10000000000), MaxValueValidator(99999999999)])
    office = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.first_name.__str__() + " " + self.last_name.__str__()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.IntegerField(validators=[MinValueValidator(10000000000), MaxValueValidator(99999999999)])
    gender = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.first_name.__str__() + " " + self.last_name.__str__()


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.DateTimeField("appointment time")


class Record(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True)
    problem = models.CharField(max_length=300)
    treatment = models.CharField(max_length=300)
    diagnosis = models.CharField(max_length=100)


class Inpatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateField("start date")
    end_date = models.DateField("end date")
    room = models.CharField(max_length=50)

    def __str__(self):
        return self.patient.__str__()

