import datetime
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


def createCD(request, name, timer):
    ip  = request.META.get("REMOTE_ADDR", "0.0.0.0")
    dev = getattr(request, "device_id", request.COOKIES.get("device_id", ""))

    cache.set(f"cd:{name}:{dev}:{ip}", timer)



def getCD(request, name):
    ip  = request.META.get("REMOTE_ADDR", "0.0.0.0")
    dev = getattr(request, "device_id", request.COOKIES.get("device_id", ""))

    device = cache.get(f"cd:{name}:{dev}:{ip}")

    if not device:
        return 0
    remainingTime = device - timezone.now()

    return int(remainingTime.total_seconds())


