from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, View
from django.http import JsonResponse
from .forms import (
    CurrentEmploymentForm, EducationTrainingForm, EmploymentHistoryForm,
    EqualityOpportunityForm, PersonalDetailsForm, RefereesForm,
)
from .models import JobApplication, Jobs


APPLICATION_SECTIONS = {
    1: ('Personal Details', PersonalDetailsForm),
    2: ('Current / Most Recent Employer', CurrentEmploymentForm),
    3: ('Previous Employment', EmploymentHistoryForm),
    4: ('Qualifications, Education and Training', EducationTrainingForm),
    5: ('Referees', RefereesForm),
    6: ('Equality of Opportunity', EqualityOpportunityForm),
}


def _json_ready(data):
    """JSONField cannot store Python date objects returned by DateField."""
    return {key: value.isoformat() if hasattr(value, 'isoformat') else value for key, value in data.items()}


def _get_submitted_job_ids(user):
    if not user.is_authenticated or user.role != 'job_seeker':
        return []
    return list(JobApplication.objects.filter(applicant=user, status='submitted').values_list('job_id', flat=True))


@login_required
def apply_for_job(request, pk):
    """Save one application section at a time, then show a final review."""
    if request.user.role != 'job_seeker':
        messages.error(request, 'Only job seeker accounts can apply for jobs.')
        return redirect('company:detail', pk=pk)

    job = get_object_or_404(Jobs, pk=pk)
    application, _ = JobApplication.objects.get_or_create(job=job, applicant=request.user)
    if application.status == 'submitted':
        messages.info(request, 'You have already submitted an application for this job.')
        return redirect('company:detail', pk=job.pk)

    try:
        step = int(request.GET.get('step', request.POST.get('step', 1)))
    except (TypeError, ValueError):
        step = 1
    step = max(1, min(step, 7))

    if step == 7:
        if request.method == 'POST' and request.POST.get('submit_application'):
            if all(str(number) in application.data for number in APPLICATION_SECTIONS):
                application.status = 'submitted'
                application.submitted_at = timezone.now()
                application.save(update_fields=['status', 'submitted_at', 'updated_at'])
                messages.success(request, 'Your application has been submitted successfully.')
                return redirect('company:detail', pk=job.pk)
            messages.error(request, 'Please complete every section before submitting.')
            return redirect(f"{reverse_lazy('company:apply', kwargs={'pk': job.pk})}?step=1")

        review_sections = []
        for number, (title, form_class) in APPLICATION_SECTIONS.items():
            form = form_class(initial=application.data.get(str(number), {}))
            review_sections.append((number, title, form))
        return render(request, 'apply.html', {
            'job': job, 'application': application, 'step': step,
            'review_sections': review_sections, 'total_steps': 6,
        })

    title, form_class = APPLICATION_SECTIONS[step]
    initial = application.data.get(str(step), {})
    form = form_class(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        application.data[str(step)] = _json_ready(form.cleaned_data)
        application.save(update_fields=['data', 'updated_at'])
        return redirect(f"{reverse_lazy('company:apply', kwargs={'pk': job.pk})}?step={step + 1}")

    return render(request, 'apply.html', {
        'job': job, 'application': application, 'form': form, 'step': step,
        'section_title': title, 'total_steps': 6, 'previous_step': step - 1 if step > 1 else None,
    })


class CreateJobs(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    success_url = reverse_lazy('company:jobs')
    template_name = 'create_job.html'
    model = Jobs
    fields = [
        'company_name',
        'company_discription',
        'company_website',
        'job_title',
        'job_category',
        'employment_type',
        'work_mode',
        'job_discription',
        'job_experience',
        'education_level',
        'number_vacancies',
        'application_deadline',
        'job_location',
        'minimum_salary',
        'job_stipend',
        'job_starting_date',
        'job_skills',
        'benefits',
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-100'
        for name in ('application_deadline', 'job_starting_date'):
            form.fields[name].widget.input_type = 'date'
        for name in ('minimum_salary', 'job_stipend'):
            form.fields[name].widget.attrs['step'] = '0.01'
        form.fields['company_discription'].widget.attrs['rows'] = 4
        return form

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employer'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first.')
            return redirect('account:login')

        if request.user.role != 'employer':
            messages.error(request, 'Only employers can post jobs.')
            return redirect('company:home')

        from profiles.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if profile.company_verification_status != 'verified':
            messages.error(request, 'Verify your company before posting a job.')
            return redirect('profiles:profile', username=request.user.username)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


def jobs(request):
    jobs = Jobs.objects.select_related('posted_by__profile').order_by('-id')
    employer_id = request.GET.get('employer')
    selected_company = None
    if employer_id:
        jobs = jobs.filter(posted_by_id=employer_id)
        selected_company = jobs.values_list('company_name', flat=True).first()
    submitted_job_ids = _get_submitted_job_ids(request.user)
    return render(request, 'jobs.html', {
        'jobs': jobs,
        'submitted_job_ids': submitted_job_ids,
        'selected_company': selected_company,
    })


def companies(request):
    """List each employer once, with a link to that employer's open jobs."""
    employers = {}
    for job in Jobs.objects.select_related('posted_by__profile').order_by('posted_by_id', '-id'):
        employer_id = job.posted_by_id
        if employer_id not in employers:
            profile = getattr(job.posted_by, 'profile', None)
            employers[employer_id] = {
                'user': job.posted_by,
                'name': (profile.company_name if profile and profile.company_name else job.company_name),
                'logo': profile.company_logo if profile and profile.company_logo else None,
                'job_count': 0,
            }
        employers[employer_id]['job_count'] += 1

    return render(request, 'companies.html', {'companies': employers.values()})


class ManageJobsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Show an employer only the jobs posted from their own account."""
    model = Jobs
    template_name = 'jobs.html'
    context_object_name = 'jobs'

    def test_func(self):
        return self.request.user.role == 'employer'

    def get_queryset(self):
        return Jobs.objects.filter(posted_by=self.request.user).select_related('posted_by__profile').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manage_page'] = True
        return context

    def handle_no_permission(self):
        messages.error(self.request, 'Only employers can manage job listings.')
        return redirect('company:home')


def home(request):
    jobs = Jobs.objects.select_related('posted_by__profile').order_by('-id')
    submitted_job_ids = _get_submitted_job_ids(request.user)
    return render(request, 'home.html', {'jobs': jobs, 'submitted_job_ids': submitted_job_ids})


class DetailPageView(DetailView):
    http_method_names = ['get']
    template_name = 'detail.html'
    model = Jobs
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submitted_job_ids'] = _get_submitted_job_ids(self.request.user)
        return context

class UpdatePageView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    # http_method_names = ['post']
    model = Jobs
    template_name = 'update_job.html'
    fields = [
            'company_name',
            'company_discription',
            'company_website',
            'job_title',
            'job_category',
            'employment_type',
            'work_mode',
            'job_discription',
            'job_experience',
            'education_level',
            'number_vacancies',
            'application_deadline',
            'job_location',
            'minimum_salary',
            'job_stipend',
            'job_starting_date',
            'job_skills',
            'benefits',
        ]
    def test_func(self):
        job = self.get_object()
        return job.posted_by == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('company:detail', kwargs={'pk': self.object.pk})

class DeleteJob(DeleteView):
    model = Jobs
    success_url = reverse_lazy('company:jobs')

    def test_func(self):
        job = self.get_object()
        return job.posted_by == self.request.user


@login_required
def get_applicants(request, job_pk):
    """API endpoint to get all applicants for a job (JSON response)."""
    job = get_object_or_404(Jobs, pk=job_pk)
    
    # Only the employer who posted the job can view applicants
    if job.posted_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    applications = JobApplication.objects.filter(job=job, status__in=['submitted', 'pending', 'shortlisted', 'rejected']).select_related('applicant')
    
    applicants_data = [
        {
            'id': app.id,
            'applicant_id': app.applicant.id,
            'applicant_name': app.applicant.username,
            'applicant_email': app.applicant.email,
            'status': app.status,
            'submitted_at': app.submitted_at.isoformat() if app.submitted_at else None,
            'updated_at': app.updated_at.isoformat() if app.updated_at else None,
        }
        for app in applications
    ]
    
    return JsonResponse({'applicants': applicants_data})


class ApplicantDetailView(LoginRequiredMixin, View):
    """View applicant's submitted application details."""
    
    def get(self, request, job_pk, application_id):
        job = get_object_or_404(Jobs, pk=job_pk)
        application = get_object_or_404(JobApplication, pk=application_id, job=job)
        
        # Only the employer who posted the job can view applicants
        if job.posted_by != request.user:
            messages.error(request, 'Unauthorized access.')
            return redirect('company:home')
        
        # Reconstruct the application data with section titles
        sections = {}
        for step_num, (title, form_class) in APPLICATION_SECTIONS.items():
            section_key = str(step_num)
            if section_key in application.data:
                sections[section_key] = {
                    'title': title,
                    'data': application.data[section_key]
                }
        
        context = {
            'job': job,
            'application': application,
            'applicant': application.applicant,
            'sections': sections,
            'APPLICATION_SECTIONS': APPLICATION_SECTIONS,
        }
        return render(request, 'applicant_detail.html', context)


@login_required
def update_applicant_status(request, application_id):
    """API endpoint to update applicant status (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    application = get_object_or_404(JobApplication, pk=application_id)
    
    # Only the employer who posted the job can update applicant status
    if application.job.posted_by != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    new_status = request.POST.get('status')
    valid_statuses = [choice[0] for choice in JobApplication.STATUS_CHOICES]
    
    if new_status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    
    application.status = new_status
    application.save(update_fields=['status', 'updated_at'])
    
    return JsonResponse({
        'success': True,
        'status': new_status,
        'message': f'Applicant status updated to {new_status}'
    })


@login_required
def get_job_seeker_applications(request):
    """API endpoint to get all applications for a job seeker (JSON response)."""
    if request.user.role != 'job_seeker':
        return JsonResponse({'error': 'Only job seekers can access this'}, status=403)
    
    applications = JobApplication.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__posted_by').order_by('-submitted_at')
    
    apps_data = [
        {
            'id': app.id,
            'job_id': app.job.id,
            'job_title': app.job.job_title,
            'company_name': app.job.company_name,
            'status': app.status,
            'status_display': app.get_status_display(),
            'submitted_at': app.submitted_at.isoformat() if app.submitted_at else None,
            'updated_at': app.updated_at.isoformat() if app.updated_at else None,
        }
        for app in applications
    ]
    
    return JsonResponse({
        'applications': apps_data,
        'count': len(apps_data),
    })


