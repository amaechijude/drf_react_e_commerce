from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers import RegisterSerializer


@api_view(["POST"])
def register_user(request: Request) -> Response:
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user_serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request: Request) -> Response:
    email = request.data.get("email")  # type: ignore
    password = request.data.get("password")  # type: ignore

    if not email or not password:
        return Response(
            {"details": "Invalid credentinals"}, status=status.HTTP_400_BAD_REQUEST
        )

    # authenticate user
    user = authenticate(email=email, password=password)
    if user is None:
        return Response(
            {"details": "Invalid credentinals"}, status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)

    response = Response({"id": user.id, "email": user.email}, status=200)  # type: ignore

    # set cookie
    response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60,
        domain="localhost",
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 2,
        domain="localhost",
        path="/",
    )

    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_view(request: Request) -> Response:
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return Response({"details": "Refresh_token not found"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        response = Response(status=status.HTTP_201_CREATED)

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24,
            domain="localhost",
            path="/",
        )
        return response
    except Exception:
        return Response(
            {"Invalid or expired refresh Token"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request: Request) -> Response:
    response = Response(status=status.HTTP_204_NO_CONTENT)

    try:
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    except Exception:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_view(request):
    user = request.user
    data = {"id": user.id, "email": user.email}
    return Response(data=data, status=200)
