from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from helmdect.settings import FIREBASE_CONFIG
from django.shortcuts import render, redirect
from django.urls import reverse
# from .models import User
import pyrebase
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth import authenticate, login as auth_login 

# Initialize Firebase Realtime Database
config = FIREBASE_CONFIG
firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL after login
    else:
        form = SignUpForm()
    return render(request, 'helmdectpages/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user:
                auth_login(request, user)
                return redirect(reverse('home'))  # Replace 'home' with your desired redirect URL after login
    else:
        form = UserLoginForm()
    return render(request, 'helmdectpages/login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('login')
    
# @login_required(login_url='/login/')
def home(request):
    return render(request, 'helmdectpages/home.html')

def about(request):
    return render(request, 'helmdectpages/about.html')

@login_required
def report_history(request):
    # Fetching all documents under the path 'test/push'
    reports = database.child("test/push").get().val()

    # Processing the retrieved reports into a context dictionary
    report_datas = {}
    if reports:
        for key, value in reports.items():
            report_datas[key] = value

    # Sort report_datas by dateTime field in descending order (latest first)
    report_datas = dict(sorted(report_datas.items(), key=lambda item: item[1].get('dateTime', ''), reverse=True))

    return render(request, 'helmdectpages/report_history.html', {'reports': report_datas})

@login_required
def data_visualization(request):
    report_fields = {
        "date": "2023-11-27",
        "time": "12:00",
        "location": "Cavite",
        "type_of_helmet": "Full Face"
    }
    
    for field, value in report_fields.items():
        set_database_value(f"reports/{field}", value)
    
    
    report_data = {
        'date': get_database_value("reports/date"),
        'time': get_database_value("reports/time"),
        'location': get_database_value("reports/location"),
        'type_of_helmet': get_database_value("reports/type_of_helmet"),
    }
    
    return render(request, 'helmdectpages/data_visualization.html', report_data)

@login_required
def detailed_reports(request):
    report_fields = {
        "number_of_motorcyclist_detected": "1",
        "color": "Red",
        "texture": "Smooth",
        "proper_usage": "Yes",
        "violations": "None"
    }
    
    for field, value in report_fields.items():
        set_database_value(f"detailed_reports/{field}", value)
    
    report_data = {
        'motorcyclist_detected': get_database_value("detailed_reports/number_of_motorcyclist_detected"),
        'plate_number': get_database_value("reports/plate_number"),
        'location': get_database_value("reports/location"),
        'time': get_database_value("reports/time"),
        'type_of_helmet': get_database_value("reports/type_of_helmet"),
        'color': get_database_value("detailed_reports/color"),
        'texture': get_database_value("detailed_reports/texture"),
        'proper_usage': get_database_value("detailed_reports/proper_usage"),
        'violations': get_database_value("detailed_reports/violations")
    }
    
    return render(request, 'helmdectpages/detailed_reports.html', report_data)

@login_required
def settings(request):
    return render(request, 'helmdectpages/settings.html')

def set_database_value(path, value):
    database.child(path).set(value)
    
def get_database_value(path):
    return database.child(path).get().val()


# def test_database():
#     # Write a test value to the database
#     database.child("test").set("Hello, Realtime DB!")

#     # Read the test value back
#     test_value = database.child("test").get().val()

#     # Print the test value
#     print(test_value)

# # Call the test function
# test_database()