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


