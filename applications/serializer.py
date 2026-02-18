from rest_framework import serializers
from .models import JobApplication


class JobApplicationStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=JobApplication.Status.choices)
