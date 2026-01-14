from django.contrib import admin
from .models import CartItem, Wishlist, Order, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total",       # ✅ FIXED
        "status",
        "payment",     # ✅ FIXED
        "created_at",
    )

    list_filter = (
        "status",
        "payment",     # ✅ FIXED
    )

    inlines = [OrderItemInline]
