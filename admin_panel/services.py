from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Product
from django.db.models.functions import TruncDate

User = get_user_model()

def dashboard_stats():
    return {
       
        "totalUsers": User.objects.filter(is_staff=False).count(),

        
        "totalOrders": Order.objects.count(),

        
        "totalRevenue": Order.objects.aggregate(
            total=Sum("total")
        )["total"] or 0,

        
        "totalProductsPurchased": Order.objects.aggregate(
            count=Count("id")
        )["count"],

        
        "productsByCategory": list(
            Product.objects.values("category")
            .annotate(count=Count("id"))
        ),

        
        "usersByStatus": {
            "active": User.objects.filter(is_active=True).count(),
            "blocked": User.objects.filter(is_active=False).count(),
        },

        
        "revenueOverTime": list(
            Order.objects.annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(amount=Sum("total"))
            .order_by("date")
        ),
    }
