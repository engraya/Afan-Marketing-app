from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

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
	error_contex = []
	if request.method == 'GET':
		context = {'form': FarmerRegistrationForm}
		return render(request, 'shop/farmerRegister.html', context)
	else:
		try:
			user = User.objects.create_user(username = request.POST['username'], password=request.POST['password'])
			user.save()
			farmerGroup = Group.objects.get_or_create(name='FARMER')
			farmerGroup[0].user_set.add(user)
			login(request, user)
			return redirect('farmerLogin')
		except IntegrityError:
			error_contex.append('That username has already been taken, Try Another one!')
			return render(request, 'shop/farmerRegister.html', {'form': FarmerRegistrationForm(), 'error_contex': error_contex})	
	return render(request, 'shop/farmerRegister.html', {'form': FarmerRegistrationForm(), 'error_contex': error_contex})



def buyerRegister(request):
	error_contex = []
	if request.method == 'GET':
		context = {'form': BuyerRegistrationForm}
		return render(request, 'shop/buyerRegister.html', context)
	else:
		if not(request.POST['username']):
			error_contex.append('Login can\'t be empty')
		elif not(request.POST['password1']):
			error_contex.append('Password can\'t be empty')
		elif not(request.POST['password2']):
			error_contex.append('Confirm Password can\'t be empty')
		elif request.POST['password1'] != request.POST['password2']:
			error_contex.append('Password did not match')
		elif len(request.POST['password1']) < 8:
			error_contex.append('Password less then 8 characters')
		else:
			try:
				user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'])
				user.save()
				buyerGroup = Group.objects.get_or_create(name='BUYER')
				buyerGroup[0].user_set.add(user)
				if user is not None:
					if user.groups.filter(name='BUYER').exists():
						login(request, user)
						return redirect('buyerLogin')
			except IntegrityError:
				error_contex.append('That username has already been taken')
				return render(request, 'buyerLogin.html', {'form': BuyerRegistrationForm(), 'error_contex': error_contex})	
		return render(request, 'shop/buyerLogin.html', {'form': BuyerRegistrationForm(), 'error_contex': error_contex})




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
					return redirect('farmerPage')
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
					return redirect('buyerLogin')
			else:
				messages.error(request, "Invalid Username or Password, Try agin later!")
		else:
			messages.error(request, "Invalid Username or Password, Try again later!")

	form = BuyerLoginForm()
	context = {'form' : form}
	return render(request, 'shop/buyerLogin.html', context)    