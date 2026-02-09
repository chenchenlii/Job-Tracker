from django import forms
from django.core import validators
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApplicationStatus(models.TextChoices):
    SAVED = "saved", "Saved"
    APPLIED = "applied", "Applied"
    INTERVIEW = "interview", "Interview"
    OFFER = "offer", "Offer"
    REJECTED = "rejected", "Rejected"
    GHOSTED = "ghosted", "Ghosted"


class LongURLField(models.TextField):
    description = "URL field with no length limit"

    def __init__(self, verbose_name=None, name=None, **kwargs):
        models.TextField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(validators.URLValidator())

    def formfield(self, **kwargs):
        # As with TextField, this will cause URL validation to be performed
        # twice.
        defaults = {
            "form_class": forms.URLField,
        }
        defaults.update(kwargs)
        return super(LongURLField, self).formfield(**defaults)


class JobApplication(models.Model):
    class JobMatchScore(models.IntegerChoices):
        ONE = 1, _("I applied because I'm desperate")
        TWO = 2, _("hm... not sure about this")
        THREE = 3, _("Fit some criteria, worth a try")
        FOUR = 4, _("It's a match!")
        FIVE = 5, _("The perfect dream job")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    platform = models.CharField(
        max_length=100,
        help_text="e.g. LinkedIn, Indeed, Company Website",
    )
    job_url = LongURLField(blank=True, null=True, help_text="Job ads link")
    applied_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date the application was submitted",
    )
    match_sore = models.IntegerField(
        choices=JobMatchScore.choices,
        default=JobMatchScore.ONE,
        help_text="How well do you think this job suits you",
    )
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus,
        default=ApplicationStatus.SAVED,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        "JobApplication", on_delete=models.CASCADE, related_name="status_history"
    )
    from_status = models.CharField(max_length=20, choices=ApplicationStatus)
    to_status = models.CharField(
        max_length=20,
        choices=ApplicationStatus,
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="application_status_changes",
        help_text="User who triggered the status change",
    )
    changed_at = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):
    class InterviewType(models.TextChoices):
        PHONE = "phone", "Phone Screen"
        TECHNICAL = "technical", "Technical"
        BEHAVIORAL = "behavioral", "Behavioral"
        ONSITE = "onsite", "Onsite"
        FINAL = "final", "Final"

    class InterviewStatus(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        PENDING = "pending", "Pending"
        PASS = "pass", "Pass"
        FAIL = "fail", "Fail"

    application = models.ForeignKey(
        "JobApplication", on_delete=models.CASCADE, related_name="interviews"
    )
    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
    )
    round = models.PositiveSmallIntegerField(
        help_text="Interview round number (1, 2, 3...)"
    )
    interview_date = models.DateTimeField()
    interviewer = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Interviewer name(s)",
    )
    interview_notes = models.TextField(blank=True, null=True)
    interview_status = models.CharField(
        max_length=20,
        choices=InterviewStatus.choices,
        default="upcoming",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["interview_date"]
        unique_together = ("application", "round")
        indexes = [
            models.Index(fields=["interview_date"]),
            models.Index(fields=["interview_status"]),
        ]
