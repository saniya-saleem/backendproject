from django.urls import path
from .views import (
    AdminTokenView,
    AdminDashboardAPIView,
    AdminUsersAPIView,
    AdminUserStatusAPIView,
    AdminProductsAPIView,
    AdminProductDetailAPIView,
    AdminOrdersAPIView,
    AdminOrderStatusAPIView,
    AdminUserOrdersAPIView,
    AdminUserDetailAPIView
)

urlpatterns = [
    # AUTH
    path("login/", AdminTokenView.as_view()),

    # DASHBOARD
    path("dashboard/", AdminDashboardAPIView.as_view()),

    # USERS
    path("users/", AdminUsersAPIView.as_view()),
    path("users/<int:pk>/", AdminUserDetailAPIView.as_view()),   # GET
    path("users/<int:pk>/status/", AdminUserStatusAPIView.as_view()),  # PATCH
    
    path("users/<int:pk>/orders/", AdminUserOrdersAPIView.as_view()),

    # PRODUCTS
    path("products/", AdminProductsAPIView.as_view()),
    path("products/<int:pk>/", AdminProductDetailAPIView.as_view()),

    # ORDERS
    path("orders/", AdminOrdersAPIView.as_view()),
    path("orders/<int:pk>/", AdminOrderStatusAPIView.as_view()),
]
