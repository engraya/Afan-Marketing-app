from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator
import json
import datetime
# Create your views here.

def landingPage(request):
	return render(request, 'shop/landingPage.html')

@login_required(login_url='landingPage')
def home(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context =  {'cartItems' : cartItems, 'order' : order, 'items' : items}
	return render(request, 'shop/home.html', context)


@login_required(login_url='landingPage')
def shop(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	product_list = Product.objects.all()
	paginator = Paginator(product_list, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'page_obj' : page_obj, 'cartItems' : cartItems, 'order' : order, 'items' : items}
	return render(request, 'shop/shopPage.html', context)

@login_required(login_url='landingPage')
def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
	return render(request, 'shop/cart.html', context)


@login_required(login_url='landingPage')
def checkOut(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
	return render(request, 'shop/checkout.html', context)

@login_required(login_url='landingPage')
def contactUs(request):
    return render(request, 'shop/contactUs.html')


def farmerClick(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('home')
	return render(request, 'shop/farmerClick.html')

    
def buyerClick(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('home')
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

@login_required(login_url='landingPage')
@user_passes_test(is_farmer)	
def addProduct(request):
	if request.method == 'POST':
		form  = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, "Product Added Successfully!.")
			return redirect("shop")
		else:
			messages.error(request, "Error Occured while Adding a New Product...!")
	else:
		form = ProductForm()
	context = {'form' : form}
	return render(request, 'shop/newProduct.html', context)			



@login_required(login_url='landingPage')
def productDetails(request, pk):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	product = Product.objects.get(id=pk)
	context = {'product' : product, 'cartItems' : cartItems, 'order' : order, 'items' : items}
	return render(request, 'shop/productDetail.html', context)

@login_required(login_url='landingPage')
@user_passes_test(is_farmer)
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	product.delete()
	return redirect('shop')


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	buyer = request.user.buyer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(buyer=buyer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


@login_required(login_url='landingPage')
@user_passes_test(is_farmer)
def recentOrders(request):
	orders = Order.objects.all()
	context = {'orders' : orders}
	return render(request, 'shop/recentOrders.html', context)


@login_required(login_url='landingPage')
def buyProceed(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'cartItems' : cartItems, 'order' : order, 'items' : items}
	return render(request, 'shop/buyProceed.html', context)	