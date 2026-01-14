from rest_framework import serializers
from products.models import Product
from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Category


User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined"]


class AdminProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "stock",
            "rating",
            "category",
        ]

    def create(self, validated_data):
        category_name = validated_data.pop("category")

        category, _ = Category.objects.get_or_create(
            name=category_name.strip().lower()
        )

        validated_data["category"] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "category" in validated_data:
            category_name = validated_data.pop("category")
            category, _ = Category.objects.get_or_create(
                name=category_name.strip().lower()
            )
            instance.category = category

        return super().update(instance, validated_data)


class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class AdminProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
