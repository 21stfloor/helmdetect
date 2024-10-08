from io import BytesIO
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from helmdect.settings import BASE_DIR, FIREBASE_CONFIG
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import pyrebase
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
import base64
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from PIL import Image
from ultralytics import YOLO

# Initialize Firebase Realtime Database
config = FIREBASE_CONFIG
firebase = pyrebase.initialize_app(config)
database = firebase.database()
model = YOLO(os.path.join(BASE_DIR, 'best.pt'))



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session with the new password
            messages.success(request, 'Your password was changed successfully.')
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }
    return render(request, 'helmdectpages/change_password.html', context)

# Create your views here.
def register(request):
    context = {}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = SignUpForm()
    context["form"] = form
    return render(request=request, template_name="helmdectpages/register.html", context=context)

class MyLoginView(LoginView):
    # form_class=LoginForm
    redirect_authenticated_user=True
    template_name='helmdectpages/login.html'

    def get_success_url(self):
        # write your logic here
        # if self.request.user.is_superuser:
        return reverse('home')# '/progress/'



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
    reports = database.child("reports").get().val()
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    if start_date_param and end_date_param:
        try:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d')
            
            filtered_reports = {}
            if reports:
                for key, value in reports.items():
                    timestamp = value.get('dateTime', 0)  # Assuming 'dateTime' is the timestamp field
                    
                    # Check if timestamp is valid
                    if isinstance(timestamp, int) and timestamp > 0:
                        try:
                            report_date = datetime.fromtimestamp(timestamp / 1000.0)
                            if start_date <= report_date <= end_date:
                                # Check and set default value for helmet_type if missing
                                if 'helmet_type' not in value:
                                    value['helmet_type'] = 'Unknown'
                                filtered_reports[key] = value
                        except (ValueError, OSError) as e:
                            # Handle conversion errors
                            pass
                        
                reports = filtered_reports

        except ValueError:
            # Handle the case when dates are not in the correct format
            pass
            
    report_datas = {}
    if reports:
        for key, value in reports.items():
            report_datas[key] = value

    # Sort report_datas by dateTime field in descending order (latest first)
    report_datas = dict(sorted(report_datas.items(), key=lambda item: item[1].get('dateTime', 0), reverse=True))

    return render(request, 'helmdectpages/report_history.html', {'reports': report_datas})



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

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        base64_string = request.POST.get('image', None)  # Assuming the base64 string is sent as a parameter named 'base64_string'
        if(base64_string is None):
            return JsonResponse({'error': 'Invalid request'}, status=400)
        # Convert base64 string to image
        decoded = base64.b64decode(base64_string)
        img = Image.open(BytesIO(decoded))

        # Run inference on the image using YOLO model
        results = model.predict(img, save=False, imgsz=320, conf=0.1)

        classes = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.data[0][-1])
                classes.append(model.names[class_id])

        return JsonResponse({'result': ' '.join(classes)})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)