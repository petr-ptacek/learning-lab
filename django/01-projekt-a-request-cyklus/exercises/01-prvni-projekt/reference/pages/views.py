import platform

import django
from django.conf import settings
from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("Ahoj z Djanga!")


def health(request):
    return JsonResponse({"status": "ok"})


def info(request):
    return JsonResponse(
        {
            "framework": "Django",
            "django_version": django.get_version(),
            "python_version": platform.python_version(),
            "debug": settings.DEBUG,
        }
    )
