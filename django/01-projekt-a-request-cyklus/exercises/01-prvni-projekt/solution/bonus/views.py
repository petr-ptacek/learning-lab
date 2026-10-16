from datetime import datetime

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils import timezone


def teapot(request: HttpRequest):
    return JsonResponse({"error": "Jsem konvice"}, status=418)


def time(request: HttpRequest):
    now_datetime = datetime.now()
    now_django = timezone.localtime()

    return JsonResponse(
        {
            "use_tz": settings.USE_TZ,
            "now_datetime": now_datetime,
            "now_django": now_django,
            "time_zone": settings.TIME_ZONE,
        }
    )
