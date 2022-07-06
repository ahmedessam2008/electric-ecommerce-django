from .models import Product
from django import forms

class ModelForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = [
      "title",
      "brand",
      "label_sale",
      "new_price",
      "category",
      "color",
      "rating",
      ]
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Text goes here'}),
      'brand': forms.Select(attrs={'class': 'form-control'}),
      'label_sale': forms.TextInput(attrs={'class': 'form-control'}),
      'new_price': forms.TextInput(attrs={'class': 'form-control'}),
      'category': forms.Select(attrs={'class': 'form-control'}),
      'color': forms.Select(attrs={'class': 'form-control'}),
      'rating': forms.TextInput(attrs={'class': 'form-control'}),
    }
    labels = {
        "new_price": "Max-Price"
    }