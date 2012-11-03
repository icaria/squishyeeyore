from django import forms
from django.forms import extras
from schoolime.models import *

class LoginForm(forms.Form):
    email = forms.CharField(max_length=75, label="Email")
    pw = forms.CharField(widget=forms.PasswordInput, label="Password")
    
class HomeForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=30, label="Last name")
    user_name = forms.CharField(max_length=30, label="User name")
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Institution")
    concentration = forms.CharField(max_length=64, label="Concentration")
    phone = forms.CharField(max_length=30, label="Phone")
    birthday = forms.DateField(widget=extras.SelectDateWidget(years=YEAR), label="Birthday")
    about = forms.CharField(widget=forms.Textarea(attrs={'cols':'40', 'rows':'5'}), label="About Me", max_length=255)
    is_verified = forms.BooleanField()

class ActivateForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=30, label="Last name")
    user_name = forms.CharField(max_length=30, label="User name")
    is_verified = forms.BooleanField()

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=30, label="Last name")
    user_name = forms.CharField(max_length=30, label="User name")
    is_verified = forms.BooleanField()

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=30, label="Last name")
    email = forms.CharField(max_length=75, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password2")