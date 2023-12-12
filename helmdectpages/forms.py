from django import forms 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()



# class UserLoginForm(forms.Form):
#     email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
#     password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts for individual fields
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class SettingsForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    new_password = forms.CharField(label='New Password', max_length=100)
    confirm_new_password = forms.CharField(label='Confirm New Password', max_length=100)
    
class ReportForm(forms.Form):
    report = forms.CharField(label='Report', max_length=100)
    date = forms.CharField(label='Date', max_length=100)
    time = forms.CharField(label='Time', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    description = forms.CharField(label='Description', max_length=100)

class DetailedReportForm(forms.Form):
    report = forms.CharField(label='Report', max_length=100)
    date = forms.CharField(label='Date', max_length=100)
    time = forms.CharField(label='Time', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    description = forms.CharField(label='Description', max_length=100)
    image = forms.ImageField(label='Image', max_length=100)
