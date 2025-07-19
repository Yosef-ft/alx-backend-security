from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.META.get('PATH_INFO')

        blocked_ips = BlockedIP.objects.values_list('ip_address', flat=True)

        if ip_address in blocked_ips:
            return HttpResponseForbidden("Your IP has been blocked")


        RequestLog.objects.create(
            ip_address=ip_address,
            path=path
        )

        response = self.get_response(request)
        return response
