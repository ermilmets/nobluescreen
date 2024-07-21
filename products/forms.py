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


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'







