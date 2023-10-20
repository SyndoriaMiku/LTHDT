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
    ('Cancel', 'Order Cancel')
)





class Item(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='produce_image/', null=True, blank=True)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY, max_length=5)
    price = models.FloatField()
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    def get_id(self):
        return self.uuid
    def __str__(self):
        return self.name
    
class Orders(models.Model):

    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    
        
    
    