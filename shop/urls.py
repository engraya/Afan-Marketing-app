from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.landingPage, name="landingPage"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkOut, name="checkout"),
    path('shop', views.shop, name="shop"),
    path('product/<int:pk>', views.productDetails, name="productDetail"),
    path('deleteProduct/<int:pk>', views.deleteProduct, name='deleteProduct'),
    path('contactUs', views.contactUs, name="contactUs"),
    path('farmerClick', views.farmerClick, name='farmerClick'),
    path('buyerClick', views.buyerClick, name='buyerClick'),

    path("afterlogin", views.afterlogin, name="afterlogin"),

    path('buyerPage', views.buyerPage, name='buyerPage'),
    path('farmerPage', views.farmerPage, name='farmerPage'),

    path('logout', views.logoutPage, name='logout'),

    path('farmerRegister', views.farmerRegister, name='farmerRegister'),
    path('farmerLogin', views.farmerLogin, name='farmerLogin'),
    path('buyerRegister', views.buyerRegister, name='buyerRegister'),
    path('buyerLogin', views.buyerLogin, name='buyerLogin'),

    path('newProduct', views.addProduct, name="newProduct"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")
]
