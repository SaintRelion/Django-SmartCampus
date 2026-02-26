from django.urls import path
from .views import (
    ActivateSessionView,
    HeartbeatView,
    DeactivateSessionView,
)

urlpatterns = [
    path("activate/", ActivateSessionView.as_view(), name="activate-session"),
    path("heartbeat/", HeartbeatView.as_view(), name="heartbeat"),
    path("deactivate/", DeactivateSessionView.as_view(), name="deactivate-session"),
]
