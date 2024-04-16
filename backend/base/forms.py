from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms


class CreateItemForm (forms.Form):
    pass


from django import forms
from .models import Item

class ItemPriceEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['price']

