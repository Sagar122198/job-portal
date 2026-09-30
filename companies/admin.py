from django.contrib import admin
from .models import JobApplication, Jobs
class CreateJob(admin.ModelAdmin):
    pass

admin.site.register(Jobs,CreateJob)
admin.site.register(JobApplication)
