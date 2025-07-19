from django.shortcuts import render

from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login
from django.shortcuts import render


def get_ratelimit_key(group, request):
    if request.user.is_authenticated:
        return request.user.pk 
    return request.META.get("REMOTE_ADDR")

@ratelimit(key=get_ratelimit_key, rate='10/m', method='POST', block=True)
@ratelimit(key=get_ratelimit_key, rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Login successful!")
        return HttpResponse("Invalid credentials", status=401)
    return render(request, 'login.html')
