from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, role='admin', **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('1', 'customer'),
        
    )
    
    role = models.CharField(max_length=19, choices=ROLE_CHOICES)
    phonenumber = models.CharField(max_length=10, default='9999999999')

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            # Add any custom permissions here if needed
        ]


# PATIENT MODELS

class PatientInfo(models.Model):
    Patientid = models.IntegerField(primary_key=True)  # Auto-generated unique identifier
    Name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Occupation = models.CharField(max_length=100)
    RecentVisit = models.DateField()

    def __str__(self):
        return self.Name

class MedicalHistory(models.Model):
    # Link medical history to PatientInfo using Patientid
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='medical_histories')
    Date = models.DateField()
    Observation = models.TextField()
    Remarks = models.TextField()

    def __str__(self):
        return f"Medical History for {self.patient.Name} on {self.Date}"

class BloodReport(models.Model):
    # Link blood report to PatientInfo using Patientid
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='blood_reports')
    Test = models.CharField(max_length=100)
    Result = models.CharField(max_length=100)
    Status = models.CharField(max_length=50)

    def __str__(self):
        return f"Blood report for {self.patient.Name}, Test: {self.Test}"

class CurrentSymptoms(models.Model):
    # Link current symptoms to PatientInfo using Patientid
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='current_symptoms')
    Symptoms = models.TextField()

    def __str__(self):
        return f"Current symptoms for {self.patient.Name}"
