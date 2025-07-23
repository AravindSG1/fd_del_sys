from django.db import models
from orders.models import Order

# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('dummy', 'Dummy'),
        ('stripe', 'Stripe'),
        ('cash on delivery', 'Cash on Delivery')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    txn_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return f"Payment of Order #{self.order.id} - {self.status}"