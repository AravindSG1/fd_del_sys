from django.db import models
from accounts.models import LoginTable

# Create your models here.
class CustomerProfile(models.Model):
    customer = models.OneToOneField(LoginTable, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='customers/profile_pic', blank=True, null=True)
    
    def __str__(self):
        return self.username