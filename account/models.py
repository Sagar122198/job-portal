from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICE =[
        ('employer' , 'Employer'),
        ('job_seeker' , 'Job Seeker')
    ]
    role=models.CharField(max_length=20, choices=ROLE_CHOICE, default='job_seeker')
    email_verified = models.BooleanField(default=False)


class EmailVerificationOTP(models.Model):
    """One active, short-lived verification code per password-signup account."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='email_otp')
    code_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() >= self.expires_at
