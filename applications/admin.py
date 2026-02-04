from django.contrib import admin

from .models import ApplicationStatusHistory, JobApplication, Interview


class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "from_status",
        "to_status",
        "changed_at",
    )

    list_filter = (
        "application",
        "from_status",
        "to_status",
    )

    search_fields = (
        "application__job_title",
        "application__company_name",
        "changed_by__email",
    )

    ordering = ("-changed_at",)


class ApplicationStatusHistoryInline(admin.TabularInline):
    model = ApplicationStatusHistory
    extra = 0
    can_delete = False
    readonly_fields = (
        "from_status",
        "to_status",
        "changed_by",
        "changed_at",
    )


class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "round",
        "interview_type",
        "interview_date",
        "interview_status",
    )

    list_filter = (
        "application",
        "interview_type",
        "interview_status",
        "interview_date",
    )

    search_fields = (
        "application__job_title",
        "application__company_name",
        "interviewer",
    )


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0
    fields = (
        "round",
        "interview_type",
        "interview_date",
        "interview_status",
    )
    ordering = ("round",)


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
    inlines = (
        ApplicationStatusHistoryInline,
        InterviewInline,
    )


admin.site.register(ApplicationStatusHistory, ApplicationStatusHistoryAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
