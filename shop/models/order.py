from django.db import models
from .products import Product
from django.contrib.auth.models import User


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"OrderItem for {self.product.name}"
    

class Order(models.Model):
    status_choice = (
        ("pending", "PENDING"),
        ("accepted", "ACCEPTED"),
        ("rejected", "REJECTED")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    items = models.ManyToManyField(OrderItem)
    address = models.CharField(max_length=300, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, choices=status_choice, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
  
    
    def __str__(self):
        return f"{self.user.username}'s order"
    

    def get_total(self):
        total = 0
        for item in self.items.all():
            total+=item.total_price

        return total
    
    