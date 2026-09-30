from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import secrets
from django.shortcuts import render, redirect
from .forms import CustomForm
from .models import CustomUser, EmailVerificationOTP


OTP_LIFETIME_MINUTES = 10
MAX_OTP_ATTEMPTS = 5


def _send_otp(user):
    code = f'{secrets.randbelow(1_000_000):06d}'
    EmailVerificationOTP.objects.update_or_create(
        user=user,
        defaults={
            'code_hash': make_password(code),
            'expires_at': timezone.now() + timedelta(minutes=OTP_LIFETIME_MINUTES),
            'attempts': 0,
        },
    )
    send_mail(
        'Verify your JobPortal email',
        f'Your JobPortal verification code is {code}. It expires in {OTP_LIFETIME_MINUTES} minutes.',
        None,
        [user.email],
        fail_silently=False,
    )


def signup(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_verified = False
            user.save()
            _send_otp(user)
            request.session['pending_verification_user_id'] = user.pk
            messages.success(request, 'We sent a 6-digit verification code to your email address.')
            return redirect('account:verify_email')
    else:
        form = CustomForm()

    return render(request, 'signup.html', {'form': form})


def verify_email(request):
    user_id = request.session.get('pending_verification_user_id')
    if not user_id:
        messages.error(request, 'Start by creating an account, then verify its email address.')
        return redirect('account:signup')

    user = get_object_or_404(CustomUser, pk=user_id)
    if user.email_verified:
        return redirect('account:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        otp = getattr(user, 'email_otp', None)
        if not code.isdigit() or len(code) != 6:
            messages.error(request, 'Enter the 6-digit code from your email.')
        elif not otp or otp.is_expired():
            messages.error(request, 'That code has expired. Request a new one below.')
        elif otp.attempts >= MAX_OTP_ATTEMPTS:
            messages.error(request, 'Too many incorrect attempts. Request a new code below.')
        elif not check_password(code, otp.code_hash):
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            messages.error(request, 'That code is not correct. Please try again.')
        else:
            user.email_verified = True
            user.is_active = True
            user.save(update_fields=['email_verified', 'is_active'])
            otp.delete()
            request.session.pop('pending_verification_user_id', None)
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )
            messages.success(request, 'Email verified successfully. Welcome to JobPortal!')
            return redirect('company:home')

    return render(request, 'verify_email.html', {'email': user.email})


def resend_otp(request):
    if request.method != 'POST':
        return redirect('account:verify_email')
    user_id = request.session.get('pending_verification_user_id')
    user = get_object_or_404(CustomUser, pk=user_id)
    if not user.email_verified:
        _send_otp(user)
        messages.success(request, 'A new verification code has been sent.')
    return redirect('account:verify_email')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.email_verified:
                request.session['pending_verification_user_id'] = user.pk
                messages.error(request, 'Verify your email before logging in.')
                return redirect('account:verify_email')
            login(request, user)
            messages.success(request, 'Welcome! You can browse and apply for jobs.')
            return redirect('company:home')
        candidate = CustomUser.objects.filter(username=request.POST.get('username', '')).first()
        if candidate and not candidate.email_verified and candidate.check_password(request.POST.get('password', '')):
            request.session['pending_verification_user_id'] = candidate.pk
            messages.error(request, 'Verify your email before logging in.')
            return redirect('account:verify_email')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})
