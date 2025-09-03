from django.db import models
from users.models import User

class Case(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='hso_cases'  # <-- unique reverse name
    )
    patient_name = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True)
    disease = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    treatment = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    surveillance_notes = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    address = models.TextField(blank=True)
    district = models.TextField(blank=True) 
    supervising_facility = models.TextField(blank=True)     
    reporting_method = models.TextField(blank=True)
    population_estimate = models.IntegerField(null=True, blank=True)
    case_source = models.TextField(blank=True)
    contact_tracing_done = models.TextField(blank=True)
    environmental_risk_factors = models.TextField(blank=True)
    vector_control_measure = models.TextField(blank=True)

    def __str__(self):
        return f"{self.disease} - {self.patient_name or 'anon'}"
      