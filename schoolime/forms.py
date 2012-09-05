from django import forms
from schoolime.models import *

class LoginForm(forms.Form):
    email = forms.CharField(max_length=75, label="Email")
    pw = forms.CharField(widget=forms.PasswordInput, label="Password")
    
class HomeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name')

class ProfileModal(forms.Form):
    pass
        
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password2")
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'user_name', 'password')
        widgets = {
                   'password': forms.PasswordInput(),
                   }

    def clean_user_name(self):
        em = self.cleaned_data['email']
        return self.cleaned_data['user_name'].strip() or em[:em.index('@')]