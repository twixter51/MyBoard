import secrets
from django.conf import settings

class EnsureDeviceIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_id = request.COOKIES.get("device_id")
        if not device_id:
            device_id = secrets.token_urlsafe(16)
            request._set_device_cookie = device_id
            
        request.device_id = device_id
        resp = self.get_response(request)

        if getattr(request, "_set_device_cookie", None):
            resp.set_cookie(
                "device_id", device_id,
                max_age=60*60*24*365*5, httponly=True, samesite="Lax",
                secure=not settings.DEBUG,
            )
        return resp