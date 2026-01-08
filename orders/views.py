from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import CartItem,Order,OrderItem
from products.models import Product
from .serializers import CartItemSerializer,WishlistSerializer,OrderSerializer
from .models import Wishlist
from django.shortcuts import get_object_or_404
from rest_framework import status

class AddToCartAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1

        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ViewCartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    
class RemoveFromCartAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=404
            )

        cart_item.delete()
        return Response(
            {"message": "Item removed from cart"},
            status=200
        )


class DecreaseCartItemAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=404
            )
  
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        else:
            cart_item.delete()
            return Response(
                {"message": "Item removed from cart"},
                status=200
            )


class AddToWishlistAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data)


class ViewWishlistAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)



class RemoveFromWishlistAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            item = Wishlist.objects.get(id=pk, user=request.user)
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Wishlist item not found"},
                status=404
            )

        item.delete()
        return Response({"message": "Removed from wishlist"})

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        items = request.data.get('items', [])

        if not items:
            return Response(
                {"error": "No items provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=request.user,
            total_amount=request.data.get('total_amount'),
            payment_method=request.data.get('payment_method'),
            address=request.data.get('address'),
            status='completed'
        )

        order_items = [
            OrderItem(
                order=order,
                product_id=item['product'],
                quantity=item['quantity'],
                price=item['product_price']
            )
            for item in items
        ]

        OrderItem.objects.bulk_create(order_items)

        return Response(
            {"message": "Order placed successfully"},
            status=status.HTTP_201_CREATED
        )


class OrderHistoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
