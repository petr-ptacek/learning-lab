from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone


def server_time(request):
    return JsonResponse(
        {
            "now": timezone.localtime().isoformat(),
            "time_zone": settings.TIME_ZONE,
        }
    )


def teapot(request):
    return JsonResponse({"error": "Jsem konvice"}, status=418)
