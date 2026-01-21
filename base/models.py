from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('policy', 'Policy Officer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
