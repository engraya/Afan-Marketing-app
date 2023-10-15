from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('shop', views.shop, name="shop"),
    path('contactUs', views.contactUs, name="contactUs"),
    path('farmerClick', views.farmerClick, name='farmerClick'),
    path('buyerClick', views.buyerClick, name='buyerClick'),

    path('buyerPage', views.buyerPage, name='buyerPage'),
    path('farmerPage', views.farmerPage, name='farmerPage'),

    path('farmerRegister', views.farmerRegister, name='farmerRegister'),
    path('farmerLogin', views.farmerLogin, name='farmerLogin'),
    path('buyerRegister', views.buyerRegister, name='buyerRegister'),
    path('buyerLogin', views.buyerLogin, name='buyerLogin'),
]
