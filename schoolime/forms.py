from django import forms
from django.forms import extras
from schoolime.models import *

class LoginForm(forms.Form):
    email = forms.CharField(max_length=75, label="Email")
    pw = forms.CharField(widget=forms.PasswordInput, label="Password")
    
class HomeForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=30, label="Last name")
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Institution")
    concentration = forms.CharField(max_length=64, label="Field of Study")
    phone = forms.CharField(max_length=30, label="Phone")
    birthday = forms.DateField(widget=extras.SelectDateWidget(years=YEAR), label="Birthday")
    about = forms.CharField(widget=forms.Textarea(attrs={'cols':'40', 'rows':'5'}), label="About Me", max_length=255)
    
    def visible_fields(self):
        invisibles = []
        invisibles.append(self.fields['first_name'])
        invisibles.append(self.fields['last_name'])
        visibles = super(HomeForm, self).visible_fields()
        return [v for v in visibles if v.field not in invisibles]
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name')

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password2")
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'user_name', 'email', 'password')
        widgets = {
                   'password': forms.PasswordInput(),
                   }
        
    def clean_user_name(self):
        em = self.cleaned_data['email']
        return self.cleaned_data['user_name'].strip() or em[:em.index('@')]
        