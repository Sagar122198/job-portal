from django.db import models
from account.models import CustomUser


class UserProfile(models.Model):
    COMPANY_VERIFICATION_CHOICES = [
        ('unverified', 'Unverified'),
        ('pending', 'Verification pending'),
        ('verified', 'Verified'),
        ('rejected', 'Verification rejected'),
    ]
    RELOCATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('open', 'Open to Opportunities'),
    ]
    
    WORK_STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('looking', 'Actively Looking'),
        ('open', 'Open to Opportunities'),
    ]

    # Link to user
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    # Personal Information
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    # cover_image = models.ImageField(upload_to='profile_covers/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Professional Information
    current_work = models.CharField(max_length=255, blank=True, help_text='Current job title or position')
    professional_summary = models.TextField(blank=True)
    key_achievements = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_links = models.TextField(blank=True, help_text='Add multiple links separated by commas')

    # Education
    degree = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    # Skills & Certifications
    certifications = models.TextField(blank=True, help_text='List certifications separated by commas')
    technical_skills = models.TextField(blank=True, help_text='List skills separated by commas')
    soft_skills = models.TextField(blank=True, help_text='List skills separated by commas')
    languages = models.TextField(blank=True, help_text='Languages and proficiency level')

    # Job Preferences
    desired_job_titles = models.CharField(max_length=255, blank=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='open')
    notice_period = models.DateField(blank=True, null=True, help_text='When you can start a new job')
    willing_to_relocate = models.CharField(max_length=10, choices=RELOCATION_CHOICES, default='open')
    expected_salary = models.CharField(max_length=100, blank=True, help_text='e.g., $50,000 - $70,000')

    # Files
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Employer / Company Information
    company_name = models.CharField(max_length=255, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    cover_banner = models.ImageField(upload_to='company_banners/', blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    company_size = models.CharField(max_length=100, blank=True)
    company_type = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    headquarters_location = models.CharField(max_length=255, blank=True)
    about_company = models.TextField(blank=True)
    official_website = models.URLField(blank=True)
    company_email = models.EmailField(blank=True)
    company_verification_status = models.CharField(max_length=20, choices=COMPANY_VERIFICATION_CHOICES, default='unverified')
    company_verification_submitted_at = models.DateTimeField(blank=True, null=True)
    x_url = models.URLField(blank=True, help_text='Company X (formerly Twitter) profile URL')
    perks_benefits = models.TextField(blank=True, help_text='List perks and benefits separated by commas')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name_plural = 'User Profiles'

