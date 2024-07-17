from django import forms
from products.models import ProductRating


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['feedback', 'star_rating']




