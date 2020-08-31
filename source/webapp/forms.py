from django import forms
from .models import CATEGORY_CHOICES, Orders
from django import forms
from webapp.models import Product
DEFAULT_CATEGORY = CATEGORY_CHOICES[0][0]


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class OrederForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['created_at']
