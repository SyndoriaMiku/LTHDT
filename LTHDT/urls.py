"""
URL configuration for LTHDT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='store/logout.html'),name='logout'),
    path('search', views.search_view,name='search'),
    
    path('adminclick', views.admin_view),
    path('adminlogin', LoginView.as_view(template_name='store/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    
    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    
    path('admin-item', views.admin_item_view,name='admin-item'),
    path('admin-add-item', views.admin_add_item_view,name='admin-add-item'),
    path('delete-item/<int:pk>', views.delete_item_view,name='delete-item'),
    path('update-item/<int:pk>', views.update_item_view,name='update-item'),
    
    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),
    
    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='store/customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),
    
    

]
