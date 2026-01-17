from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsAdmin
from .serializers import (
    AdminUserSerializer,
    AdminOrderSerializer,
    AdminProductWriteSerializer,
    AdminProductReadSerializer,

)
from .auth_serializers import AdminTokenSerializer
from .services import dashboard_stats
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

User = get_user_model()


class AdminTokenView(TokenObtainPairView):
    serializer_class = AdminTokenSerializer


class AdminUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.filter(is_staff=False)
        return Response(AdminUserSerializer(users, many=True).data)

class AdminProductsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        qs = Product.objects.all()
        return Response(
            AdminProductReadSerializer(qs, many=True).data
        )

    def post(self, request):
        serializer = AdminProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)



class AdminOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        orders = Order.objects.select_related("user").all()
        return Response(AdminOrderSerializer(orders, many=True).data)


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response(dashboard_stats())


class AdminOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")

        allowed = ["Pending", "Shipped", "Delivered"]
        if new_status not in allowed:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save()

        return Response(
            {"message": "Order status updated", "status": new_status},
            status=status.HTTP_200_OK,
        )
        
class AdminUserStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        
        user.is_active = not user.is_active
        user.save()

        return Response(
            {
                "id": user.id,
                "is_active": user.is_active
            },
            status=status.HTTP_200_OK
        )



class AdminProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = AdminProductWriteSerializer(
            product, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
# admin/views.py

class AdminUserOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        orders = Order.objects.filter(user_id=pk)
        return Response(AdminOrderSerializer(orders, many=True).data)

class AdminUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(AdminUserSerializer(user).data)
