from datetime import timedelta
import uuid
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ActiveSession


class ActivateSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        existing = ActiveSession.objects.filter(
            user=request.user, is_active=True
        ).first()

        if existing:
            if timezone.now() - existing.last_seen > timedelta(seconds=30):
                existing.is_active = False
                existing.save()
            else:
                return Response(
                    {"session_allowed": False}, status=status.HTTP_403_FORBIDDEN
                )

        ActiveSession.objects.update_or_create(
            user=request.user,
            defaults={
                "session_id": str(uuid.uuid4()),
                "is_active": True,
                "last_seen": timezone.now(),
            },
        )

        return Response({"session_allowed": True})


class DeactivateSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ActiveSession.objects.filter(user=request.user).update(is_active=False)

        return Response({"deactivated": True})


class HeartbeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ActiveSession.objects.filter(user=request.user).update(last_seen=timezone.now())

        return Response({"alive": True})
