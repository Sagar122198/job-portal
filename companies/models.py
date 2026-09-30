from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
class Jobs(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'), ('part_time', 'Part Time'),
        ('internship', 'Internship'), ('contract', 'Contract'),
    ]
    WORK_MODE_CHOICES = [('remote', 'Remote'), ('hybrid', 'Hybrid'), ('onsite', 'On-site')]

    
    company_name = models.CharField(max_length=100)
    company_discription = models.CharField(max_length=250)
    company_website = models.URLField(blank=True)
    job_title = models.CharField(max_length=100)
    job_category = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='onsite')
    job_discription = models.TextField()
    job_experience= models.IntegerField()
    education_level = models.CharField(max_length=100, blank=True)
    number_vacancies = models.PositiveIntegerField(default=1)
    application_deadline = models.DateField(blank=True, null=True)
    job_location = models.CharField(max_length=100)
    minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_stipend = models.DecimalField(max_digits=10 , decimal_places=2) 
    job_starting_date = models.CharField(max_length=20)
    job_skills = models.CharField(max_length=255)
    benefits = models.JSONField(default=list, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name


class JobApplication(models.Model):
    """A job seeker's saved draft or submitted application for a job."""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected')
    ]

    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    data = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job', 'applicant'], name='unique_job_application_per_applicant'),
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.applicant.username} - {self.job.job_title}'
