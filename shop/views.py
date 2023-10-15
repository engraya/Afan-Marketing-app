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

# Create your views here.

def landingPage(request):
	return render(request, 'shop/landingPage.html')


def home(request):
    return render(request, 'shop/home.html')


def cart(request):
    return render(request, 'shop/cart.html')


    
def checkout(request):
    return render(request, 'shop/checkout.html')


def shop(request):
    return render(request, 'shop/shopPage.html')


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
