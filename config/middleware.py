import os
from django.http import HttpResponseForbidden


class AdminIPRestrictionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ip = os.getenv("ALLOWED_ADMIN_IP")

    def __call__(self, request):

        if request.path.startswith("/admin"):

            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

            if x_forwarded_for:
                user_ip = x_forwarded_for.split(",")[0].strip()
            else:
                user_ip = request.META.get("REMOTE_ADDR")

            if self.allowed_ip and user_ip != self.allowed_ip:
                return HttpResponseForbidden("Admin access denied")

        return self.get_response(request)