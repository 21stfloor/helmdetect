from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def register(request):
    return render(request, 'helmdectpages/register.html')

def login(request):
    return render(request, 'helmdectpages/login.html')

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