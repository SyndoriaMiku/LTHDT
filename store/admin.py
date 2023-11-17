from django.contrib import admin
from .models import Item, Customer, Order

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','phone')
    search_fields = ['user']
admin.site.register(Customer, CustomerAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','number','category','price')
    search_fields = ['name','number']
admin.site.register(Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)