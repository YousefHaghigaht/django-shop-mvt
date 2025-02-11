from django import forms


class QuantityForm(forms.Form):
    quantity = forms.IntegerField()