from django.urls import path
from .views import (ProductListAPIView,ProductDetailAPIView,ProductByCategoryAPIView )      
from home.views import BannerAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path('products/category/<str:category_name>/', ProductByCategoryAPIView.as_view()),
    
    path('banners/', BannerAPIView.as_view()),   
]
