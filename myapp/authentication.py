from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from ratelimit.exceptions import Ratelimited
from ratelimit.decorators import ratelimit

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        ip_address = self.get_client_ip(request)
        self.check_ip_block(ip_address)
        return super().authenticate(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def check_ip_block(self, ip_address):
        if settings.IP_BLOCK_COUNT and settings.IP_BLOCK_TIME:
            key = f'login_attempts:{ip_address}'
            attempts = cache.get(key, 0)
            if attempts >= settings.IP_BLOCK_COUNT:
                raise AuthenticationFailed('Too many login attempts. Your IP is blocked for a while.')
            return attempts

    @ratelimit(key='ip', rate='3/m', method=ratelimit.ALL, block=True)
    def handle_rate_limit(self, request, *args, **kwargs):
        raise Ratelimited()