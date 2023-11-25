from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from helmdect.settings import FIREBASE_CONFIG
from .forms import RegisterForm, LoginForm, SettingsForm, ReportForm, DetailedReportForm
from .models import User
import pyrebase

# Initialize Firebase Realtime Database
config = FIREBASE_CONFIG
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email      = form.cleaned_data['email']
            password   = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if password == confirm_password:
                user = User(email=email, password=password, confirm_password=confirm_password)
                user.save()
                return HttpResponse("User created successfully")
            else:
                return HttpResponse("Password and Confirm Password does not match")
        else:
            return HttpResponse("Invalid Form")
    else:
        form = RegisterForm()
        return render(request, 'helmdectpages/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email, password=password).first()
            
            if user:
                request.session['user_id'] = user.id
                return render(request, 'helmdectpages/home.html')
            else:
                return HttpResponse("Invalid Credentials")
        else:
            return HttpResponse("Invalid Form")
    else:
        form = LoginForm()
        return render(request, 'helmdectpages/login.html', {'form': form})

    
@login_required(login_url='/login/')
def home(request):
    return render(request, 'helmdectpages/home.html')

def report_history(request):
    return render(request, 'helmdectpages/report_history.html')

def data_visualization(request):
    return render(request, 'helmdectpages/data_visualization.html')

def detailed_reports(request):
    return render(request, 'helmdectpages/detailed_reports.html')

def settings(request):
    return render(request, 'helmdectpages/settings.html')



# def test_database():
#     # Write a test value to the database
#     database.child("test").set("Hello, Realtime DB!")

#     # Read the test value back
#     test_value = database.child("test").get().val()

#     # Print the test value
#     print(test_value)

# # Call the test function
# test_database()