from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


def home_view(request):
    items = models.Item.objects.all()
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'store/index.html', {'items' :items, 'item_count_in_cart' : item_count_in_cart})

def admin_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect("adminlogin")

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm,'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,"store/customersignup.html", context=mydict)

def is_customer(user):
    return user.groups.filter(name="CUSTOMER").exists()

def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

#----Admin----

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    #
    customercount = models.Customer.objects.all().count()
    itemcount = models.Item.objects.all().count()
    ordercount = models.Order.objects.all().count()
    
    
    #for Order
    orders = models.Order.objects.all()
    ordered_items = []
    ordered_bys = []
    for order in orders:
        ordered_item = models.Item.objects.all().filter(id=order.item.id)
        ordered_by = models.Customer.objects.all().filter(id=order.customer.id)
        ordered_items.append(ordered_item)
        ordered_bys.append(ordered_by)
        
    mydict = {
        'customercount' : customercount,
        'itemcount' : itemcount,
        'ordercount' : ordercount,
        'data' : zip(ordered_items, ordered_bys, orders)
        
    }
    return render(request, 'store/admin_dashboard.html', context=mydict)



@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers = models.Customer.objects.all()
    return render(request, 'store/view_customer.html', {'customers': customers})

@login_required(login_url='adminlogin')
def delete_customer_view(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')

@login_required(login_url='adminlogin')
def update_customer_view(request, pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES, instance=customer)
    mydict={'userForm' : userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm=forms.CustomerUserForm(request.POST, instance=user)
        customerForm=forms.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
        return render(request,'store/admin_update_customer.html', context=mydict)

#-----Item-----
    
@login_required(login_url='adminlogin')
def admin_item_view(request):
    items = models.Item.objects.all()
    return render(request, 'store/admin_item.html', {'items': items})

@login_required(login_url='adminlogin')
def admin_add_item_view(request):
    itemForm = forms.ItemForm()
    if request.method == 'POST':
        itemForm = forms.ItemForm(request.POST, request.FILES)
        if itemForm.is_valid():
            itemForm.save()
        return HttpResponseRedirect('admin-item')
    return render(request, 'store/admin_add_item.html', {'itemForm': itemForm})
    
@login_required(login_url='adminlogin')
def delete_item_view(request, pk):
    item = models.Item.objects.get(id=pk)
    item.delete()
    return redirect('admin-item')

@login_required(login_url='adminlogin')
def update_item_view(request, pk):
    item = models.Item.objects.get(id=pk)
    itemForm = forms.ItemForm(instance=item)
    if request.method == 'POST':
        itemForm = forms.ItemForm(request.POST, request.FILES, instance=item)
        if itemForm.is_valid():
            itemForm.save()
        return redirect('admin-item')
    return render(request, 'store/admin_update_item.html', {'itemForm': itemForm})


#-----Order-----


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders = models.Order.objects.all()
    ordered_items = []
    ordered_bys = []
    for order in orders:
        ordered_item = models.Item.objects.all().filter(id=order.item.id)
        ordered_by = models.Customer.objects.all().filter(id=order.customer.id)
        ordered_items.append(ordered_item)
        ordered_bys.append(ordered_by)
    return render(request, 'store/admin_view_booking.html', {'data': zip(ordered_items, ordered_bys, orders)})

@login_required(login_url='adminlogin')
def delete_order_view(request, pk):
    order = models.Order.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

@login_required(login_url='adminlogin')
def update_order_view(request, pk):
    order = models.Order.objects.get(id=pk)
    orderForm = forms.OrderForm(instance=order)
    if request.method == 'POST':
        orderForm = forms.OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
        return redirect('admin-view-booking')
    return render(request, 'store/update_order.html', {'orderForm': orderForm})

#-----------------------
#----Public Customer----
#-----------------------

def search_view(request):
    query = request.GET['query']
    items = models.Item.objects.filter(name__icontains=query)
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
    word = "Search result for " + query
    
    if request.user.is_authenticated:
        return render(request, 'store/customer_home.html', {'items': items, 'word': word, 'item_count_in_cart' : item_count_in_cart})
    return render(request, 'store/index.html', {'items': items, 'word': word, 'item_count_in_cart' : item_count_in_cart})


def add_to_cart_view(request, pk):
    items = models.Item.objects.all()
    
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 1
    
    response = render(request, 'store/index.html', {'items': items, 'item_count_in_cart' : item_count_in_cart})
    
    # adding item id to cookies
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        if item_ids == "":
            item_ids = str(pk)
        else:
            item_ids = item_ids + "|" + str(pk)
        response.set_cookie('item_ids', item_ids)
    else:
        response.set_cookie('item_ids', pk)
    
    item = models.Item.objects.get(id=pk)
    
    return response

#check out cart
def cart_view(request):
    #cart counter
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
    
    #fetching item details from database with id from cookies
    items = None
    total = 0
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        if item_ids != "":
            item_id_in_cart = item_ids.split('|')
            items = models.Item.objects.all().filter(id__in=item_id_in_cart)
            
            #check total price
            for item in items:
                total = total + item.price
    return render(request, 'store/cart.html', {'items': items, 'total': total, 'item_count_in_cart' : item_count_in_cart})

def remove_from_cart_view(request, pk):
    #cart counter
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
        
    #removing item id from cookies
    total=0
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        item_id_in_cart = item_ids.split('|')
        item_id_in_cart = list(set(item_id_in_cart))
        item_id_in_cart.remove(str(pk))
        items = models.Item.objects.all().filter(id__in=item_id_in_cart)
        
        #adjust total price after removing item
        for item in items:
            total = total + item.price
            
        #update cookies after removing item
        value=""
        for i in range(len(item_id_in_cart)):
            if i == 0:
                value = value + item_id_in_cart[0]
            else:
                value = value + "|" + item_id_in_cart[i]
        response = render(request, 'store/cart.html', {'items': items, 'total': total, 'item_count_in_cart' : item_count_in_cart})
        if value == "":
            response.delete_cookie('item_ids')
        response.set_cookie('item_ids', value)
        return response

#----------------------------------------
#-----------Customer View----------------
#----------------------------------------

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    items = models.Item.objects.all()
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
    return render(request, 'store/customer_home.html', {'items': items, 'item_count_in_cart' : item_count_in_cart})


#Shipments address
@login_required(login_url='customerlogin')
def customer_address_view(request):
    #checking cart before showing address
    item_count_in_cart = False
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        if item_ids != "":
            item_count_in_cart = True
    #counter in cart
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        counter = item_ids.split('|')
        item_count_in_cart = len(set(counter))
    else:
        item_count_in_cart = 0
        
    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            #getting address from user here
            phone = addressForm.cleaned_data['Phone']
            address = addressForm.cleaned_data['Address']
            #showing total price
            total = 0
            if 'item_ids' in request.COOKIES:
                item_ids = request.COOKIES['item_ids']
                if item_ids != "":
                    item_id_in_cart = item_ids.split('|')
                    items = models.Item.objects.all().filter(id__in=item_id_in_cart)
                    for item in items:
                        total = total + item.price
                        
            response = render(request, 'store/payment.html', {'total' : total})
            response.set_cookie('phone', phone)
            response.set_cookie('address', address)
            return response
    return render(request, 'store/customer_address.html', {'addressForm': addressForm, 'item_count_in_cart' : item_count_in_cart, 'item_count_in_cart' : item_count_in_cart})
    
    
    
#payment success check
@login_required(login_url='customerlogin')
def payment_success_view(request):
    #Place order after payment success
    #Creating order in database
    #Delete cookies after order placed
    customer = models.Customer.objects.get(user_id=request.user.id)
    items = None
    phone = None
    address = None
    if 'item_ids' in request.COOKIES:
        item_ids = request.COOKIES['item_ids']
        if item_ids != "":
            item_id_in_cart = item_ids.split('|')
            items = models.Item.objects.all().filter(id__in=item_id_in_cart)
            

    if 'phone' in request.COOKIES:
        phone = request.COOKIES['phone']
    if 'address' in request.COOKIES:
        address = request.COOKIES['address']
        
    for item in items:
        models.Order.objects.get_or_create(customer=customer, item=item, phone=phone, address=address, status='Pending')
    
    #delete cookies after order placed
    response = render(request, 'store/payment_success.html')
    response.delete_cookie('item_ids')
    response.delete_cookie('phone')
    response.delete_cookie('address')
    return response


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_orders_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    orders = models.Order.objects.all().filter(customer_id=customer)
    ordered_items = []
    for order in orders:
        ordered_item = models.Item.objects.all().filter(id=order.item.id)
        ordered_items.append(ordered_item)

    return render(request, 'store/my_orders.html', {'data': zip(ordered_items, orders)})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'store/my_profile.html', {'customer': customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(instance=customer)
    mydict = {'userForm': userForm,'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
        return HttpResponseRedirect('my-profile')
    return render(request, 'store/edit_profile.html', context=mydict)






