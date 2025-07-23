from django.db import models
from accounts.models import LoginTable
from restaurants.models import FoodItem

# Create your models here.
class Cart(models.Model):
    customer = models.OneToOneField(LoginTable, on_delete=models.CASCADE,
                limit_choices_to={'is_customer':True}, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.customer.username}"
    
    def total(self):
        return sum([item.subtotal() for item in self.items.all()])
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.food_item.name} X {self.quantity}"   
    
    def subtotal(self):
        return self.food_item.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('out_of_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(LoginTable, on_delete=models.CASCADE, limit_choices_to={'is_customer':True})
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='orders')  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    placed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"order #{self.id}-> {self.customer.username} ({self.status})"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_status = None

        if not is_new:
            old_status = Order.objects.get(pk=self.pk).status
            print('checkpoint1----------------------------------------')

        super().save(*args, **kwargs)

        if old_status != 'ready' and self.status == 'ready':
            print('checkpoint2----------------------------------------')
            from delivery.utils import auto_assign_agent_to_order
            auto_assign_agent_to_order(self) 
            print('checkpoint3----------------------------------------')   

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
    

