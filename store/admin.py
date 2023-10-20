from django.contrib import admin
from .models import Item, Customer, Orders

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','phone')
    search_fields = ['name']
admin.site.register(Customer, CustomerAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','number','category','price')
    search_fields = ['name','number']
admin.site.register(Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)