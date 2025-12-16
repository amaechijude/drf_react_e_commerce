from typing import Any
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token


class JWTCookieAuthentication(JWTAuthentication):
    """
    Custome authentication to read read jwt from cookie instead of header
    """

    def authenticate(self, request: Request) -> tuple[Any, Token] | None:
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
