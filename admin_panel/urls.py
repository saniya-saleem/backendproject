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
)

urlpatterns = [
    # AUTH
    path("login/", AdminTokenView.as_view()),

    # DASHBOARD
    path("dashboard/", AdminDashboardAPIView.as_view()),

    # USERS
    path("users/", AdminUsersAPIView.as_view()),
    path("users/<int:pk>/", AdminUserStatusAPIView.as_view()),

    # PRODUCTS
    path("products/", AdminProductsAPIView.as_view()),
    path("products/<int:pk>/", AdminProductDetailAPIView.as_view()),

    # ORDERS
    path("orders/", AdminOrdersAPIView.as_view()),
    path("orders/<int:pk>/", AdminOrderStatusAPIView.as_view()),
]
