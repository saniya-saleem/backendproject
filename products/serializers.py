from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "stock",
            "rating",
            "category",        # for POST / PUT
            "category_name",   # for GET
        ]

    def create(self, validated_data):
        category_name = validated_data.pop("category")

        category, _ = Category.objects.get_or_create(
            name=category_name.strip().lower()
        )

        validated_data["category"] = category
        return super().create(validated_data)
