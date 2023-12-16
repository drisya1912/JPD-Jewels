from django import forms

from administrator.models import Offer
from user_account.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'address', 'place', 'pincode', 'phone']


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your coupon code',
    }))


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['product', 'discount_type', 'discount_value', 'start_date', 'end_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'discount_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'discount_value': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }