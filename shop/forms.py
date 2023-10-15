from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *



class FarmerRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Last Name'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Email'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})


    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']



class BuyerRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Last Name'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Username'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Email'})
        self.fields['password'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter your Password'})


    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class FarmerLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'

class BuyerLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Username'})
        self.fields['password'].widget.attrs.update({'class' : 'input100', 'placeholder' : 'Password'})
        
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = '__all__'


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter your Product Name", })
        self.fields["price"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter your Product price",})
        self.fields["description"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Enter Product Description",})
        self.fields["image"].widget.attrs.update({"class": "form-control unicase-form-control", "placeholder" : "Choose your Product Image",})

    class Meta:
        model = Product
        fields = '__all__'




class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'