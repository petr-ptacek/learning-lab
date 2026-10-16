from platform import python_version

from django import get_version
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse


def home(request):
    return HttpResponse("Ahoj z Djanga!")


def health(request: HttpRequest):
    return JsonResponse({"status": "ok"})


def info(request: HttpRequest):
    data = dict(
        framework="Django",
        django_version=get_version(),
        python_version=python_version(),
        debug=settings.DEBUG,
    )

    return JsonResponse(data)
