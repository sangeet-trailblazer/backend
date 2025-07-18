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
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        
    )
    fullname= models.CharField(max_length=70,default='abc')
    role = models.CharField(max_length=19, choices=ROLE_CHOICES)
    phonenumber = models.CharField(max_length=10, null=False, blank=False)
    first_name=models.CharField(max_length= 20)
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    #permissions if necessary
    class Meta: 
        permissions = []


# PATIENT MODELS

class PatientInfo(models.Model):
    CrNo = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Occupation = models.CharField(max_length=100)
    ConsultingDoctor = models.CharField(max_length=100, null=True)  # This field was incorrectly named in your view
    Diagnosis = models.CharField(max_length=100, null=True)
    FirstVisit = models.DateField(null=True)

    def __str__(self):
        return self.Name
    

class RecentVists(models.Model):
    CrNo = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='recent_visists')
    RecentVisit = models.DateField()
    Followup=models.CharField(default=0)
    



class Diagnosis(models.Model):
    # Link current symptoms to PatientInfo using Patientid
    CrNo = models.ForeignKey(PatientInfo, on_delete=models.CASCADE, related_name='diagnosis')
    Diagnosis = models.TextField()

    def __str__(self):
        return f"Current symptoms for {self.CrNo}"


class OTPStore(models.Model):
    username = models.CharField(max_length=100)
    otp = models.CharField(max_length=4)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.username} - Verified: {self.verified}"
    
