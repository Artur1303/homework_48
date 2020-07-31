from django import forms
from .models import CATEGORY_CHOICES

DEFAULT_CATEGORY = CATEGORY_CHOICES[0][0]


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    description = forms.CharField(max_length=2000, required=True, label='Описание')
    category = forms.ChoiceField(label='Категория',
                                choices=CATEGORY_CHOICES, initial=DEFAULT_CATEGORY)
    amount = forms.IntegerField(label='Остаток', min_value=0)
    price = forms.DecimalField(label='Цена', max_digits=7, decimal_places=2, min_value=0)

