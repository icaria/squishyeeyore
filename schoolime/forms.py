from django import forms
from schoolime.models import *

class LoginForm(forms.Form):
    email = forms.CharField(max_length=75, label="Email")
    pw = forms.CharField(widget=forms.PasswordInput, label="Password")
    
class HomeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name')
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student