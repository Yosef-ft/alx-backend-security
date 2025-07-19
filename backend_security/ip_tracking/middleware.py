from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
from django.core.cache import cache
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.META.get('PATH_INFO')

        blocked_ips = BlockedIP.objects.values_list('ip_address', flat=True)

        if ip_address in blocked_ips:
            return HttpResponseForbidden("Your IP has been blocked")
        

        cache_key = f"geo:{ip_address}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            try:
                response = requests.get(
                    f"http://api.ipstack.com/{ip_address}",
                    params={"access_key": os.environ.get("GEO_IP")}
                )
                data = response.json()
                print("RESPONSE", data)
                geo_data = {
                    'country': data.get('country_name'),
                    'city': data.get('city')
                }
                cache.set(cache_key, geo_data, 60 * 60 * 24)
            except Exception as e:
                geo_data = {'country': None, 'city': None}            


        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )

        response = self.get_response(request)
        return response


    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip