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
    report_fields = {
        "plate_number": "1234",
        "helmet": "Yes",
        "object_detected": "No",
        "person_detected": "Yes",
        "image": "https://firebasestorage.googleapis.com/v0/b/helmdetect.appspot.com/o/sample%20image.png?alt=media&token=9933e2d0-eaf1-4db3-954c-968e187fe168"
    }

    for field, value in report_fields.items():
        set_database_value(f"reports/{field}", value)

    report_data = {
        'plate_number': get_database_value("reports/plate_number"),
        'helmet': get_database_value("reports/helmet"),
        'object_detected': get_database_value("reports/object_detected"),
        'person_detected': get_database_value("reports/person_detected"),
        'image': get_database_value("reports/image")
    }

    return render(request, 'helmdectpages/report_history.html', report_data)
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