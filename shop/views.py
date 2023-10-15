from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder


# Create your views here.

def landingPage(request):
	return render(request, 'shop/landingPage.html')


def home(request):
    return render(request, 'shop/home.html')

def shop(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products' : products, 'cartItems' : cartItems}
	return render(request, 'shop/shopPage.html', context)


def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
	return render(request, 'shop/cart.html', context)



def checkOut(request):
	data = cartData(reuqest)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
	return render(request, 'shop/checkout.html', context)


def contactUs(request):
    return render(request, 'shop/contactUs.html')


def farmerPage(request):
	return render(request, 'shop/farmerPage.html')


def buyerPage(request):
	return render(request, 'shop/buyerPage.html')


def farmerClick(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('afterlogin')
	return render(request, 'shop/farmerClick.html')

    
def buyerClick(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('afterlogin')
	return render(request, 'shop/buyerClick.html')





def farmerRegister(request):
	form = FarmerRegistrationForm()
	if request.method == 'POST':
		form = FarmerRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			farmerGroup = Group.objects.get_or_create(name='FARMER')
			farmerGroup[0].user_set.add(user)
			return HttpResponseRedirect('farmerLogin')
		
	context = {'form' : form}
	return render(request, 'shop/farmerRegister.html', context)	



def buyerRegister(request):
	form = BuyerRegistrationForm()
	if request.method == 'POST':
		form = BuyerRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			buyerGroup = Group.objects.get_or_create(name='BUYER')
			buyerGroup[0].user_set.add(user)
			return HttpResponseRedirect('buyerLogin')
		
	context = {'form' : form}
	return render(request, 'shop/buyerRegister.html', context)	



def is_farmer(user):
    return user.groups.filter(name='FARMER').exists()
def is_buyer(user):
    return user.groups.filter(name='BUYER').exists()



def afterlogin(request):
    if is_farmer(request.user):
        return redirect('farmerPage')
    elif is_buyer(request.user):
            return redirect('buyerPage')




def farmerLogin(request):
	if request.method == 'POST':
		form = FarmerLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.groups.filter(name='FARMER').exists():
					login(request, user)
					messages.info(request, 'You are now Loggged in as Farmer')
					return redirect('home')
			else:
				messages.error(request, "Invalid Username or Password, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = FarmerLoginForm()
	context = {'form' : form}
	return render(request, 'shop/farmerLogin.html', context)


def buyerLogin(request):
	if request.method == 'POST':
		form = BuyerLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.groups.filter(name='BUYER').exists():
					login(request, user)
					messages.info(request, 'You are now Loggged in as Buyer')
					return redirect('home')
			else:
				messages.error(request, "Invalid Username or Password, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = BuyerLoginForm()
	context = {'form' : form}
	return render(request, 'shop/buyerLogin.html', context)    


def logoutPage(request):
	logout(request)
	return redirect('/')

	
def addProduct(request):
	if request.method == 'POST':
		form  = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, "Product Added Successfully!.")
			return redirect("shopPage")
		else:
			messages.error(request, "Error Occured while Adding a New Product...!")
	else:
		form = ProductForm()
	context = {'form' : form}
	return render(request, 'shop/newProduct.html', context)			



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)