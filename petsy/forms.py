from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from petsy.models import *
from django import forms
from django.forms import Textarea, NumberInput, TextInput, DateTimeInput
from django.forms import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserPetsy
        fields = ('email',
                  'username',
                  'password',
                  'password2')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['nameProduct', 'description', 'price', 'category', 'materials', 'img']
        widgets = {
            'nameProduct': forms.TextInput(attrs={'placeholder': 'En pocas palabras...',  'class': 'formulari'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Añade información relevante como estado, modelo, color...'}),
            'price': forms.NumberInput(attrs={'step': '0,1', 'class': 'precio'}),
            'category': forms.Select(attrs={'class': 'categoria'}, choices=Product.CATEGORIES),
            'materials': forms.TextInput(attrs={'class': 'formulari', 'placeholder': 'Dinos de que está hecho tu producto...'}),
            'img': forms.FileInput(attrs={'id': 'input-fa', 'accept': 'image/*', 'class': 'file'})
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["title", "message", "rating"]

        widgets = {
            "title": TextInput(attrs={'class': 'form-control', 'style': 'width:100%; resize:none'}),
            "message": Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'width:100%; resize:none'}),
            # "date": DateTimeInput(attrs={'class': 'form-control', 'style': 'width:100%; resize:none'}) ,
            "rating": NumberInput(attrs={'min': '1', 'max': '5', 'default': 1, 'style': 'display:none'})
        }

    def clean_message(self):
        """
        Check that the message contains at least one character. If not, adds an error to the form.
        :return: Message of the review
        """
        message = self.cleaned_data["message"]
        if len(message) <= 0:
            self.add_error("message", "You can't send an empty message")
            raise ValidationError("You can't send an empty message")
        return message


class Shop(forms.ModelForm):

    model = Product
    fields = ['shop_name']



