from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=500)
    country = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp}"
    

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=128)

    def __str__(self):
        return f"IP blocked {self.ip_address}"
    
class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"    