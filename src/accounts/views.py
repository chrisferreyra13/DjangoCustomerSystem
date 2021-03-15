from typing import ContextManager
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import fields, inlineformset_factory
from .models import *
from .forms import OrderForm
# Create your views here.

def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()

    totalCustomers=customers.count()
    totalOrders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={
        'orders':orders, 
        'customers':customers, 
        'totalCustomers': totalCustomers,
        'totalOrders':totalOrders,
        'delivered':delivered,
        'pending':pending,
    }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products=Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

def customer(request, pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    ordersCount=orders.count()
    context={'customer': customer, 'orders':orders, 'ordersCount':ordersCount}
    return render(request, 'accounts/customer.html',context)

def createOrder(request,pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset=orderFormSet(queryset= Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        #print('Printing POST:', request.POST)
        formset=orderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'accounts/orderForm.html',context)

def updateOrder(request, pk):

    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)

    if request.method=='POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'accounts/orderForm.html',context)

def deleteOrder(request, pk):
    order=Order.objects.get(id=pk)
    if request.method=="POST": #esto es porq el form es POST
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'accounts/delete.html',context)