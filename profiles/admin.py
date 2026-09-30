from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_email', 'company_verification_status', 'company_verification_submitted_at')
    list_filter = ('company_verification_status',)
    search_fields = ('user__username', 'company_name', 'company_email')
    list_editable = ('company_verification_status',)
