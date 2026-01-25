from django import forms
from .models import Category, Product, Address
from .validators import validate_polish_zip, validate_blik_code, validate_card_number, validate_card_date, validate_cvv, validate_no_negative


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProductForm(forms.ModelForm):
    price = forms.CharField(
        validators=[validate_no_negative],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price', 'step': '0.01'})
    )
    inventory = forms.CharField(
        validators=[validate_no_negative],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product inventory'})
    )
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'inventory', 'category', 'image']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
                   'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
                   'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select category'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)


class AddressForm(forms.ModelForm):

    zip_code = forms.CharField(
        validators=[validate_polish_zip],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00-000'})
    )
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'zip_code']

        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
        }

class CardForm(forms.Form):

    card_number = forms.CharField(
        validators=[validate_card_number],
        label = 'Numer Karty',
        max_length= 16,
        min_length= 16,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '0000 0000 0000 0000'}))

    card_owner = forms.CharField(label = 'Właściciel',
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Imie Nazwisko'}))

    expiry_date = forms.CharField(
        validators=[validate_card_date],
        label = 'Data ważności',
        max_length= 5,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'MM/YY'}))

    cvv = forms.CharField(
        validators=[validate_cvv],
        label = 'CVV',
        max_length= 3,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '123'}))

class BlikForm(forms.Form):
    blik_code = forms.CharField(
        validators=[validate_blik_code],
        label = 'Kod BLIK',
        max_length= 6,
        min_length= 6,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '000 000'}))
