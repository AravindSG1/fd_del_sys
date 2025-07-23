from django.db import models
from accounts.models import LoginTable
from orders.models import Order

# Create your models here.
class DeliveryAgentProfile(models.Model):
    agent = models.OneToOneField(LoginTable, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='delivery/profile_pic', blank=True, null=True)

class DeliveryAssignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),   
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_assignment')
    delivery_agent = models.ForeignKey(LoginTable, on_delete=models.CASCADE,
                                        limit_choices_to={'is_delivery':True},related_name='delivery_assignments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #Get previous status before save
        if self.pk:
            old_status = DeliveryAssignment.objects.get(pk=self.pk).status
        else:
            old_status = None

        super().save(*args, **kwargs)
        # Automatically update order status based on assignment status
        if self.status == 'picked_up':
            self.order.status = 'out_of_delivery'
        elif self.status == 'delivered':
            self.order.status = 'delivered'
        elif self.status == 'cancelled':
            self.order.status = 'cancelled'

        self.order.save() #save updated order

    def __str__(self):
        return f"order #{self.order.id}-> {self.delivery_agent.username} ({self.status})"
    
