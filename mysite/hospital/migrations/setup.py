
from django.db import migrations
from django.contrib.auth.models import Group


def create_groups(apps, schema_editor):
    doctors_group = Group(name="Doctors")
    patient_group = Group(name="Patients")
    doctors_group.save()
    patient_group.save()


def create_departments(apps, schema_editor):
    Department = apps.get_model("hospital", "Department")
    cardiology = Department("Cardiology",
                            "The Cardiology Department at our hospital is dedicated to providing exceptional care for "
                            "patients with cardiovascular conditions. Our team of highly skilled cardiologists, "
                            "nurses, and technicians is committed to delivering comprehensive and personalized "
                            "treatment options.", 20)
    cardiology.save()
    general_surgery = Department("General surgery",
                                 "The General Surgery department specializes in performing various surgical "
                                 "procedures to"
                                 "treat a wide range of medical conditions, including appendectomies and hernia "
                                 "repairs."
                                 "Highly skilled surgeons utilize advanced techniques to ensure optimal patient care "
                                 "and"
                                 "recovery.", 20)
    general_surgery.save()
    neurology = Department("Neurology",
                           "The Neurology department focuses on diagnosing and treating disorders of the "
                           "nervous system. Experienced neurologists use advanced diagnostic tools to identify "
                           "conditions such as epilepsy, stroke, and Alzheimer's disease. They provide "
                           "personalized treatment plans to manage and improve patients' neurological health.", 20)
    neurology.save()
    psychiatry = Department("Psychiatry",
                            "The Psychiatry department is dedicated to the diagnosis and treatment of mental "
                            "health disorders. Compassionate psychiatrists offer comprehensive evaluations and "
                            "provide therapy and counseling services. They also prescribe medications when "
                            "necessary to help individuals achieve mental well-being.", 20)
    psychiatry.save()
    oncology = Department("Oncology",
                          "The Oncology department specializes in the diagnosis, treatment, and management of "
                          "cancer. Multidisciplinary teams of oncologists, radiation therapists, and surgeons "
                          "work together to provide personalized care. They offer various treatment "
                          "modalities, including chemotherapy, radiation therapy, and surgical interventions, "
                          "to ensure the best possible outcomes for cancer patients.", 20)
    oncology.save()


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
