from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class JobApplication(models.Model):
    class JobMatchScore(models.IntegerChoices):
        ONE   = 1, _("I applied because I'm desperate")
        TWO   = 2, _("hm... not sure about this")
        THREE = 3, _("Fit some criteria, worth a try")
        FOUR  = 4, _("It's a match!")
        FIVE  = 5, _("The perfect dream job")

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        GHOSTED = "ghosted", "Ghosted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    job_title = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    platform = models.CharField(
        max_length=100,
        help_text="e.g. LinkedIn, Indeed, Company Website",
    )
    job_url = models.URLField(blank=True, null=True, help_text="Job ads link")
    applied_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date the application was submitted",
    )
    match_sore = models.IntegerField(
        choices=JobMatchScore.choices,
        default=JobMatchScore.ONE,
        help_text="How well do you think this job suits you"
    )
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.SAVED,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"



