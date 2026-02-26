from django.db import models


class ActiveSession(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
