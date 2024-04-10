from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import Department, Patient, Doctor, Appointment, Record, Inpatient
from .forms import createUserForm, patientForm, LoginForm


def index(request):
    departments_list = Department.objects.all()
    template = loader.get_template("hospital/index.html")
    context = {
        "departments_list": departments_list,
    }
    return HttpResponse(template.render(context, request))


def departments(request):
    departments_list = Department.objects.all()
    template = loader.get_template("hospital/departments.html")
    context = {
        "departments_list": departments_list,
    }
    return HttpResponse(template.render(context, request))


def staff(request):
    doctors_list = Doctor.objects.all()
    template = loader.get_template("hospital/staff.html")
    context = {
        "doctors_list": doctors_list,
    }
    return HttpResponse(template.render(context, request))


def register(request):
    form = createUserForm(request.POST)
    patient_form = patientForm(request.POST)
    if request.method == 'POST':
        if form.is_valid() and patient_form.is_valid():
            user = form.save()
            patient_group = Group.objects.get(name='Patients')
            user.groups.add(patient_group)
            profile = patient_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Your account has been successfully created')

            return redirect('login')

    context = {'form': form, 'patient_form': patient_form}
    return render(request, "hospital/register.html", context)


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'hospital/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

        messages.error(request, f'Invalid username or password')
        return render(request, 'hospital/login.html', {'form': form})


def patient_account(request, user_id):
    try:
        patient = Patient.objects.get(user__id=user_id)
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    return render(request, "hospital/patient-account.html", {"patient": patient})


def patient_visits(request, user_id):
    try:
        patient = Patient.objects.get(user__id=user_id)
        visits = Appointment.objects.filter(patient__exact=patient)
        previous_visits = []
        upcoming_visits = []
        for visit in visits:
            if Record.objects.filter(appointment__exact=visit):
                previous_visits.append(visit)
            else:
                upcoming_visits.append(visit)
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    return render(request, "hospital/patient-visits.html", {"previous_visits": previous_visits,
                                                            "upcoming_visits": upcoming_visits})


def patient_appointment(request, user_id):
    try:
        patient = Patient.objects.get(user__id=user_id)
        doctors_list = Doctor.objects.all()

        if request.method == "POST":
            doctor = Doctor.objects.get(id=request.POST['doctors'])
            time = request.POST['time']
            if Appointment.objects.filter(time=request.POST['time']).filter(doctor=doctor):
                messages.error(request, f'This time is already taken')
            # time string format: YYYY-MM-DDThh:mm
            # here we get two last characters (representing minutes) in the time string, convert them to integer
            # and check if they are divisible by 30
            # appointments can be booked each 30 minutes
            elif int(time[14:16]) % 30 != 0:
                messages.error(request, f'The minutes value should be divisible by 30')
            else:
                messages.success(request, f'Appointment is successfully created')
                appointment = Appointment(patient=patient, doctor=doctor, time=time)
                appointment.save()

    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    return render(request, "hospital/appointment.html", {"patient": patient, "doctors_list": doctors_list})


def doctor_account(request, user_id):
    try:
        doctor = Doctor.objects.get(user__id=user_id)
    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist")
    return render(request, "hospital/doctor-account.html", {"doctor": doctor})


def doctor_record(request, user_id):
    try:
        doctor = Doctor.objects.get(user__id=user_id)
        all_appointments = Appointment.objects.filter(doctor__exact=doctor)
        appointments = []
        for appointment in all_appointments:
            if Record.objects.filter(appointment__exact=appointment):
                continue
            else:
                appointments.append(appointment)
        if request.method == "POST":
            appointment = Appointment.objects.get(id=request.POST['appointment'])
            problem = request.POST['problem']
            treatment = request.POST['treatment']
            diagnosis = request.POST['diagnosis']
            if problem != "" and treatment != "" and diagnosis != "":
                patient_record = Record(appointment=appointment, problem=problem,
                                        treatment=treatment, diagnosis=diagnosis)
                patient_record.save()
            else:
                messages.error(request, f'Please fill in all the fields')

    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist")
    return render(request, "hospital/doctor-new-record.html", {"doctor": doctor, "appointments": appointments})


def doctor_records(request, user_id):
    try:
        doctor = Doctor.objects.get(user__id=user_id)
        appointments = Appointment.objects.filter(doctor__exact=doctor)
        upcoming_appointments = []
        previous_appointments = []
        # checking if there is a record for each appointment
        for appointment in appointments:
            if Record.objects.filter(appointment__exact=appointment):
                previous_appointments.append(appointment)
            else:
                upcoming_appointments.append(appointment)
    except Patient.DoesNotExist:
        raise Http404("Doctor does not exist")
    return render(request, "hospital/doctor-records.html", {"upcoming_appointments": upcoming_appointments,
                                                            "previous_appointments": previous_appointments})


def record(request, user_id, appointment_id):
    try:
        patient_record = Record.objects.get(appointment__id=appointment_id)
    except Doctor.DoesNotExist:
        raise Http404("Record does not exist")
    return render(request, "hospital/doctor-record.html", {"record": patient_record})


def user_logout(request):
    logout(request)
    return redirect('index')


def delete_appointment(request, user_id, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('patient_visits', user_id)


def doctor_inpatient(request, user_id):
    try:
        doctor = Doctor.objects.get(user__id=user_id)
        department = doctor.department
        inpatient_info = Inpatient.objects.filter(department__exact=department)
    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist")
    return render(request, "hospital/doctor-inpatient.html", {"department": department, "inpatient": inpatient_info})


def doctor_new_inpatient(request, user_id):
    try:
        doctor = Doctor.objects.get(user__id=user_id)
        department = doctor.department
        patients = Patient.objects.all()
        if request.method == "POST":
            patient = Patient.objects.get(id=request.POST['patient'])
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            room = request.POST['room']
            if start_date != "" and end_date != "" and room != "" and department.free_beds > 0:
                inpatient = Inpatient(patient=patient, department=department,
                                      start_date=start_date, end_date=end_date,
                                      room=room)
                inpatient.save()
                department.free_beds -= 1
                department.save()
            else:
                messages.error(request, f'Not all fields are filled, or no free beds')

    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist")
    return render(request, "hospital/doctor-new-inpatient.html", {"department": department, "patients": patients})


def delete_inpatient(request, user_id, inpatient_id):
    inpatient = Inpatient.objects.get(id=inpatient_id)
    department = inpatient.department
    department.free_beds += 1
    department.save()
    inpatient.delete()
    return redirect('doctor_inpatient', user_id)

