from django.db import models
from django.conf  import settings
from products.models import Product


User= settings.AUTH_USER_MODEL


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    class Meta:
        unique_together = ('user','product')
    
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    class Meta:
        unique_together = ('user', 'product')
        
        
        
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
)
    status = models.CharField(max_length=30, default='pending')
    payment_method =models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    