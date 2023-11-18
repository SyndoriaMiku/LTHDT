from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password' : forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields = ['phone']
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields=['name', 'number', 'image', 'description', 'category','price']
        
class AddressForm(forms.Form):
    Phone = forms.CharField();
    Address = forms.CharField(max_length=500)
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields=['status']
        