from django.contrib import admin

from .models import JobApplication


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("user_id", "job_title", "company_name", "platform", "applied_at")


admin.site.register(JobApplication, JobApplicationAdmin)
