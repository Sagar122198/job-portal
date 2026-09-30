from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    JOB_SEEKER_FIELDS = {
        'full_name', 'phone_number', 'location', 'current_work',
        'professional_summary', 'key_achievements', 'linkedin_url', 'portfolio_links',
        'degree', 'institution', 'graduation_year', 'certifications', 'technical_skills',
        'soft_skills', 'languages', 'desired_job_titles', 'work_status', 'notice_period',
        'expected_salary', 'willing_to_relocate', 'resume',
    }
    EMPLOYER_FIELDS = {
        'profile_picture', 'company_name', 'company_logo', 'cover_banner', 'tagline', 'industry',
        'company_size', 'company_type', 'founded_year', 'headquarters_location',
        'about_company', 'official_website', 'company_email', 'x_url', 'perks_benefits',
    }

    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        if role == 'employer':
            for field_name in self.JOB_SEEKER_FIELDS:
                self.fields.pop(field_name, None)
        elif role == 'job_seeker':
            for field_name in self.EMPLOYER_FIELDS:
                self.fields.pop(field_name, None)

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'phone_number', 'location', 'profile_picture',
            'current_work', 'professional_summary', 'key_achievements', 'linkedin_url',
            'portfolio_links', 'degree', 'institution', 'graduation_year',
            'certifications', 'technical_skills', 'soft_skills', 'languages',
            'desired_job_titles', 'work_status', 'notice_period', 'expected_salary', 'willing_to_relocate', 'resume',
            'company_name', 'company_logo', 'cover_banner', 'tagline', 'industry', 'company_size',
            'company_type', 'founded_year', 'headquarters_location', 'about_company', 'official_website',
            'company_email', 'x_url', 'perks_benefits'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'current_work': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'professional_summary': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 4}),
            'key_achievements': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 4}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'portfolio_links': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'degree': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'institution': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'certifications': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'technical_skills': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'soft_skills': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'languages': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 3}),
            'desired_job_titles': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'work_status': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'notice_period': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'expected_salary': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'willing_to_relocate': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'resume': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'company_logo': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'accept': 'image/*'}),
            'cover_banner': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'accept': 'image/*'}),
            'tagline': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'industry': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'company_size': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'e.g., 51-200 employees'}),
            'company_type': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'founded_year': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'min': 1}),
            'headquarters_location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'about_company': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 5}),
            'official_website': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'https://example.com'}),
            'company_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'}),
            'x_url': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'placeholder': 'https://x.com/company'}),
            'perks_benefits': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500', 'rows': 4}),
        }
