from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP
from django.db.models import Count

SENSITIVE_PATHS = ['/admin', '/api/login', ]

@shared_task
def flag_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)

    ip_hits = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
    )

    sensitive_ips = set(
        RequestLog.objects.filter(
            timestamp__gte=one_hour_ago,
            path__in=SENSITIVE_PATHS
        ).values_list('ip_address', flat=True)
    )

    for hit in ip_hits:
        ip = hit['ip_address']
        count = hit['request_count']
        reasons = []

        if count > 100:
            reasons.append(f'Excessive requests: {count} in the last hour')

        if ip in sensitive_ips:
            reasons.append('Accessed sensitive path')

        if reasons:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': '; '.join(reasons)}
            )