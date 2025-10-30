from uuid import UUID
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Product, Vendor
from core.permissions import IsVendor
from core.serializers import ProductSerializer, RegisterSerializer, VendorSerializer


@api_view(["POST"])
def register_user(request: Request) -> Response:
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def become_vendor(request: Request) -> Response:
    user = request.user
    if user.is_vendor:
        return Response({"details":"User is already a vendor"}, status=status.HTTP_403_FORBIDDEN)
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        user.is_vendor = True
        user.is_customer = False
        # In production activate with OTP or Magic Link via email
        serializer.save(user=user, is_activated=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsVendor])
@parser_classes([MultiPartParser, FormParser])
def create_product(request: Request) -> Response:
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return Response({"details": "Only vendors can create products"}, status=400)
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(vendor=vendor)
        return Response(data=serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsVendor])
@parser_classes([MultiPartParser, FormParser])
def update_product(request: Request, id: UUID):
    try:
        product = Product.objects.get(id=id)
        vendor = Vendor.objects.get(user=request.user)
    except (Product.DoesNotExist, Vendor.DoesNotExist) as e:
        return Response({"details": e}, status=404)
    
    if product.vendor != vendor:
        return Response({"details":"Unauthorised"}, status=403)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
        
    return Response(serializer.errors, status=404)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsVendor])
def delete_product(request: Request, id: UUID):
    try:
        product = Product.objects.get(id=id)
        vendor = Vendor.objects.get(user=request.user)
    except (Product.DoesNotExist, Vendor.DoesNotExist):
        return Response({"details": "product not found"}, status=404)
    
    if product.vendor != vendor:
        return Response({"details":"Unauthorised"}, status=403)
    
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
   


@api_view(["GET"])
def product_details(request: Request, id: UUID) -> Response:
    product = get_object_or_404(Product, id=id)
    psz = ProductSerializer(product)
    return Response(data=psz.data, status=200)


@api_view(["GET"])
def list_products(request: Request) -> Response:
    products = Product.objects.select_related("vendor").all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=200)