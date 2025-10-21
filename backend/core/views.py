from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.permissions import IsVendor
from core.serializers import RegisterSerializer


@api_view(["POST"])
def register_user(request) -> Response:
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
    
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request) -> Response:
    return Response(RegisterSerializer(request.user).data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsVendor])
def vendor_only_view(request) -> Response:
    return Response({"message": "Welcome, vendor!"}, status=status.HTTP_200_OK)