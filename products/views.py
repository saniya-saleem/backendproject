from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Category
from .serializers import ProductSerializer


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many= True)
        return Response(serializer.data)
    
# class ProductDetailAPIView(APIView):
#     def get(self, request, pk):
#         product = Product.objects.get(id=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=404
            )

        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductByCategoryAPIView(APIView):
    def get(self,request, category_name):
        products = Product.objects.filter(category_name=category_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    