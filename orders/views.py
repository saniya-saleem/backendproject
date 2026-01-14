from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import CartItem, Order, OrderItem, Wishlist
from products.models import Product
from .serializers import CartItemSerializer, WishlistSerializer, OrderSerializer
import razorpay
from django.conf import settings
from decimal import Decimal


# ---------------- CART ----------------

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        cart_item.quantity = cart_item.quantity + 1 if not created else 1
        cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_200_OK
        )


class ViewCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(
            CartItem,
            id=pk,
            user=request.user
        )
        cart_item.delete()
        return Response({"message": "Item removed from cart"})


class DecreaseCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart_item = get_object_or_404(
            CartItem,
            id=pk,
            user=request.user
        )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data)
        else:
            cart_item.delete()
            return Response({"message": "Item removed from cart"})


# ---------------- WISHLIST ----------------

class AddToWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        wishlist_item, _ = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        return Response(WishlistSerializer(wishlist_item).data)


class ViewWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)


class RemoveFromWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(
            Wishlist,
            id=pk,
            user=request.user
        )
        item.delete()
        return Response({"message": "Removed from wishlist"})


# ---------------- CHECKOUT ----------------



class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = Decimal("0")
        for item in cart_items:
            total += item.product.price * item.quantity

        order = Order.objects.create(
            user=request.user,
            customer=request.data.get("name"),
            email=request.data.get("email"),
            phone=request.data.get("phone"),
            city=request.data.get("city"),
            state=request.data.get("state"),
            pincode=request.data.get("pincode"),
            address=request.data.get("address"),
            payment=request.data.get("payment"),  # ✅ IMPORTANT
            total=total,
            status="Pending",
        )

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in cart_items
        ]

        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()  # ✅ clear cart

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )



# ---------------- ORDER HISTORY ----------------

class OrderHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)





class RazorpayOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = Decimal(request.data.get("amount"))

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": int(amount * 100),  # ₹ → paise
            "currency": "INR",
            "payment_capture": 1
        })

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order["amount"]
        })

class RazorpayVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": request.data["razorpay_order_id"],
                "razorpay_payment_id": request.data["razorpay_payment_id"],
                "razorpay_signature": request.data["razorpay_signature"],
            })
   
            return Response({"status": "success"})

        except:
            return Response(
                {"status": "failed"},
                status=status.HTTP_400_BAD_REQUEST
            )



# views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem

class ClearCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared successfully"})
