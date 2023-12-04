from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('P', 'Pack'),
    ('C', 'Card')
)

STATUS = (
    ('Pending', 'Pending'),
    ('Confirmed','Order Confirm'),
    ('Delivered', 'Order Delivered'),
    ('Canceled', 'Order Cancel')
)

class Item(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='produce_image/', null=True, blank=True, default='produce_image/nopng.jpg')
    description = models.TextField(null=True)
    category = models.CharField(choices=CATEGORY, max_length=5)
    price = models.PositiveBigIntegerField()
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True)
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.name
    
class Order(models.Model):

    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    address = models.CharField(max_length=200, default="Take at store")
    phone = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    
        
    
    