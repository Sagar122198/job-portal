from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from account.models import CustomUser
from companies.models import Jobs, JobApplication
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(DetailView):
    http_method_names = ['get']
    model = CustomUser
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_template_names(self):
        """Render the profile layout that matches the profile owner's role."""
        if self.get_object().role == 'employer':
            return ['employer_profile.html']
        return ['profile.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        context['profile'] = profile
        context['is_own_profile'] = self.request.user == user
        context['active_jobs'] = Jobs.objects.none()
        
        if user.role == 'employer':
            context['active_jobs'] = Jobs.objects.filter(posted_by=user)
        elif user.role == 'job_seeker':
            # Get job applications for job seekers
            context['job_applications'] = JobApplication.objects.filter(
                applicant=user
            ).select_related('job', 'job__posted_by').order_by('-submitted_at')
            context['application_count'] = context['job_applications'].count()
        
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    success_url = None

    def get_template_names(self):
        """Employers edit company details; job seekers edit personal details."""
        if self.request.user.role == 'employer':
            return ['employer_profile_update.html']
        return ['profile_update.html']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = self.request.user.role
        return kwargs

    def get_object(self, queryset=None):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profiles:profile', kwargs={'username': self.request.user.username})


@login_required
def submit_company_verification(request):
    """Submit a completed employer profile for an administrator's review."""
    if request.method != 'POST' or request.user.role != 'employer':
        return redirect('company:home')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.company_verification_status == 'verified':
        messages.info(request, 'Your company is already verified.')
    elif not all([profile.company_name, profile.official_website, profile.company_email]):
        messages.error(request, 'Add your company name, official website, and company email before requesting verification.')
        return redirect('profiles:profile-update')
    else:
        profile.company_verification_status = 'pending'
        profile.company_verification_submitted_at = timezone.now()
        profile.save(update_fields=['company_verification_status', 'company_verification_submitted_at'])
        messages.success(request, 'Your company verification request has been submitted for review.')
    return redirect('profiles:profile', username=request.user.username)

