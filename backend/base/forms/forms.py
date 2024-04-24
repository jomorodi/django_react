from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.
from django import forms
from base.models.models import Item


class CreateItemForm (forms.Form):
    pass

class ItemPriceEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['price']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image' ] 