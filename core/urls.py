from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("sr_libs.authentication.urls")),
    path("api/device/", include("sr_libs.fingerprint.urls")),
    path("api/otp/", include("sr_libs.otp.urls")),
]
