from django import forms


INPUT = {'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none'}
TEXTAREA = {'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none', 'rows': 4}


class SectionForm(forms.Form):
    """Base form that gives all application fields a consistent presentation."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', INPUT['class'])


class PersonalDetailsForm(SectionForm):
    forename = forms.CharField(label='Forename')
    surname = forms.CharField(label='Surname (Family Name)')
    title = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    known_as = forms.CharField(required=False)
    email = forms.EmailField()
    contact_address = forms.CharField(widget=forms.Textarea(attrs=TEXTAREA))
    permanent_home_address = forms.CharField(widget=forms.Textarea(attrs=TEXTAREA))
    telephone_number = forms.CharField(required=False)
    mobile_number = forms.CharField(required=False)
    work_number = forms.CharField(required=False)
    permission_to_work = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No'), ('requires_sponsorship', 'Requires sponsorship')])


class CurrentEmploymentForm(SectionForm):
    ever_worked_for_university_of_nottingham = forms.ChoiceField(label='Have you ever worked for University of Nottingham?', choices=[('yes', 'Yes'), ('no', 'No')])
    employer_organisation = forms.CharField(label="Employer's Organisation", required=False)
    position_held = forms.CharField(required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={**INPUT, 'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={**INPUT, 'type': 'date'}))
    notice_period = forms.CharField(required=False)
    salary_paid = forms.CharField(label='Salary Paid', required=False)
    benefits_package = forms.CharField(label='Additional Benefits / Package Information', required=False, widget=forms.Textarea(attrs=TEXTAREA))
    duties = forms.CharField(label='Brief Description of Duties', required=False, widget=forms.Textarea(attrs=TEXTAREA))
    reasons_for_leaving = forms.CharField(label='Reasons for Leaving / Change of Role', required=False, widget=forms.Textarea(attrs=TEXTAREA))


class EmploymentHistoryForm(SectionForm):
    previous_employment_records = forms.CharField(help_text='List each employer, role, start/end dates, duties, and reason for leaving.', widget=forms.Textarea(attrs={**TEXTAREA, 'rows': 10}))
    employment_gaps = forms.CharField(label='Gaps in Employment History', required=False, help_text='Explain any gaps and their dates.', widget=forms.Textarea(attrs=TEXTAREA))


class EducationTrainingForm(SectionForm):
    education_records = forms.CharField(label='Education', help_text='For each qualification include institution, start/end dates, qualification, year, type, subject, status, and grade/result.', widget=forms.Textarea(attrs={**TEXTAREA, 'rows': 10}))
    skills_training = forms.CharField(label='Relevant Skills Training', required=False, help_text='Include skill/course, provider, and whether accredited or attended.', widget=forms.Textarea(attrs=TEXTAREA))
    professional_memberships = forms.CharField(label='Professional Memberships / Accreditation', required=False, widget=forms.Textarea(attrs=TEXTAREA))


class RefereesForm(SectionForm):
    referee_1_type = forms.CharField(label='Referee 1 Type')
    referee_1_name = forms.CharField(label='Referee 1 Name')
    referee_1_position = forms.CharField(label='Referee 1 Position')
    referee_1_relationship = forms.CharField(label='Referee 1 Relationship to you')
    referee_1_address = forms.CharField(label='Referee 1 Address', widget=forms.Textarea(attrs=TEXTAREA))
    referee_1_email = forms.EmailField(label='Referee 1 Email')
    referee_1_telephone = forms.CharField(label='Referee 1 Telephone Number')
    referee_1_contact_permission = forms.ChoiceField(label='Can referee 1 be contacted without prior permission?', choices=[('yes', 'Yes'), ('no', 'No')])
    referee_2_type = forms.CharField(label='Referee 2 Type', required=False)
    referee_2_name = forms.CharField(label='Referee 2 Name', required=False)
    referee_2_position = forms.CharField(label='Referee 2 Position', required=False)
    referee_2_relationship = forms.CharField(label='Referee 2 Relationship to you', required=False)
    referee_2_address = forms.CharField(label='Referee 2 Address', required=False, widget=forms.Textarea(attrs=TEXTAREA))
    referee_2_email = forms.EmailField(label='Referee 2 Email', required=False)
    referee_2_telephone = forms.CharField(label='Referee 2 Telephone Number', required=False)
    referee_2_contact_permission = forms.ChoiceField(label='Can referee 2 be contacted without prior permission?', required=False, choices=[('yes', 'Yes'), ('no', 'No')])


class EqualityOpportunityForm(SectionForm):
    sex = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={**INPUT, 'type': 'date'}))
    gender_identity = forms.CharField(label='Gender identity', required=False)
    gender_role_different_at_birth = forms.ChoiceField(label='Do you live and work full-time in a gender role different from that assigned at birth?', required=False, choices=[('', 'Prefer not to say'), ('yes', 'Yes'), ('no', 'No')])
    nationality = forms.CharField(required=False)
    sexual_orientation = forms.CharField(required=False)
    religion = forms.CharField(required=False)
    ethnic_origin = forms.CharField(required=False)
    disability_equality_act = forms.ChoiceField(label='Do you have a disability as defined by the Equality Act?', required=False, choices=[('', 'Prefer not to say'), ('yes', 'Yes'), ('no', 'No')])
