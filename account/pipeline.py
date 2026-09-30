"""Social-auth pipeline hooks."""


def mark_google_email_verified(backend, user=None, *args, **kwargs):
    """Google has already verified the email address used for sign-in."""
    if user and backend.name == 'google-oauth2' and (not user.email_verified or not user.is_active):
        user.email_verified = True
        user.is_active = True
        user.save(update_fields=['email_verified', 'is_active'])
    return {}
