from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.serializers import RegisterSerializer, VendorSerializer


@api_view(["POST"])
def register_user(request) -> Response:
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def become_vendor(request) -> Response:
    user = request.user
    if user.is_vendor:
        return Response({"error": "Already a vendor"}, status=status.HTTP_403_FORBIDDEN)
    vendor_serializer = VendorSerializer(request.data)
    if vendor_serializer.is_valid():
        vendor = vendor_serializer.save(user=user)
        vendor.activate() # type: ignore
        vendor.save() # type: ignore
        
        return Response({"message": "Congratulations"}, status=status.HTTP_201_CREATED)
    
    return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
