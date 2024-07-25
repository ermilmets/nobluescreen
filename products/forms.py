from django import forms
from products.models import ProductRating, Order


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['feedback', 'star_rating']


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    credit_card = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit Card'}))
    exp_date = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    cvc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'}))


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    credit_card = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit Card'}))
    exp_date = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    cvc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'}))
    # (max_value=999, attrs={'class': 'form-control', 'placeholder': 'Card Number'}, min_length=3))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']







