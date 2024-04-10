from django.contrib import admin

from .models import Doctor
from .models import Patient
from .models import Department
from .models import Appointment
from .models import Record
from .models import Inpatient

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Appointment)
admin.site.register(Record)
admin.site.register(Inpatient)


