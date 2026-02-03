from django.contrib import admin

from .models import JobApplication


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "company_name", "platform", "applied_at")
    raw_id_fields = ("user",)
    list_filter = (
        "status",
        "platform",
        "applied_at",
        "created_at",
    )
    search_fields = (
        "job_title",
        "company_name",
        "platform",
        "user__email",
    )


admin.site.register(JobApplication, JobApplicationAdmin)
