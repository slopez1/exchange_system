import OpenSSL.crypto
from django.conf import settings
from django.http import HttpResponseForbidden
from django.urls import resolve

from core.middleware.CASecurityMiddleware import CASecurityMiddleware


class EndpointCASecurityMiddleware(CASecurityMiddleware):

    def _need_to_apply_this_middleware(self, request):
        # Override on chills to customize this url affected for the middleware
        path = request.path_info
        resolved = resolve(path)
        if resolved.app_name == 'endpoint':
            return True
        else:
            return False

