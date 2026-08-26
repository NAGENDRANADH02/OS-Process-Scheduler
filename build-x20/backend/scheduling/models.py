from django.db import models

class SchedulingRun(models.Model):
    algorithm = models.CharField(max_length=40)
    time_quantum = models.PositiveIntegerField(null=True, blank=True)
    inputs = models.JSONField()
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
