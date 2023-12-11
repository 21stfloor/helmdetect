from django import forms 

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

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
