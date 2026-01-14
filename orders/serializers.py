from rest_framework import serializers
from .models import CartItem
from products.models import Product
from .models import Wishlist
from .models import Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source = 'product.name')
    product_price = serializers.ReadOnlyField(source ='product.price')
    product_image = serializers.CharField(
        source="product.image",
        read_only=True
    )
    
    
    class Meta :
        model = CartItem
        fields = ['id','product','product_name','product_price','quantity','product_image']
        
        
        
class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.CharField(
        source="product.image",
        read_only=True
    )


    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_name', 'product_price','product_image']
        
        
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "email",
            "phone",
            "city",
            "state",
            "pincode",
            "address",
            "payment",     # ✅ FIXED
            "total",       # ✅ FIXED
            "status",
            "created_at",
            "items",       # ✅ MUST BE INCLUDED
        ]
