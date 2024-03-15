from django import forms
import re
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label=_('First Name'))
    last_name = forms.CharField(max_length=50, label=_('Last Name'))
    email = forms.EmailField(label=_('Email'))
    phone_number = forms.CharField(max_length=12, label=_('Phone Number'))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Repeat Password'))
    

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError(_("Password has to be at least 8 characters long."))

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(_("Password has to contain at least 1 capital letter."))

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(_("Password has to contain at least 1 small letter."))

        if not re.search(r'[0-9]', password):
            raise forms.ValidationError(_("Password has to contain at least 1 digit."))

        return password

    
class LoginForm(forms.Form):
    username = forms.EmailField(label=_('Email'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'))

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label=_('First Name'))
    last_name = forms.CharField(max_length=50, label=_('Last Name'))
    email = forms.EmailField(label=_('Email'))
    phone_number = forms.CharField(max_length=12, label=_('Phone Number'))
