from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import JobApplication, ApplicationStatusHistory
from .serializers import JobApplicationStatusUpdateSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users only access their own applications
        return JobApplication.objects.filter(user=self.request.user)

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        application = get_object_or_404(self.get_queryset(), pk=pk)

        serializer = JobApplicationStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]
        old_status = application.current_status

        if old_status == new_status:
            return Response(
                {"detail": "Status is already set to this value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            application.current_status = new_status
            application.save(update_fields=["current_status", "updated_at"])

            ApplicationStatusHistory.objects.create(
                application=application,
                from_status=old_status,
                to_status=new_status,
                changed_by=request.user,
            )

        return Response(
            {
                "message": "Status updated successfully.",
                "application_id": application.id,
                "old_status": old_status,
                "new_status": new_status,
            },
            status=status.HTTP_200_OK,
        )
