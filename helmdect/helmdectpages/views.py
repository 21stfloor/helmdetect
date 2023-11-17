from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def register(request):
    return render(request, 'helmdectpages/register.html')

def login(request):
    return render(request, 'helmdectpages/login.html')

def home(request):
    return render(request, 'helmdectpages/home.html')

def reportHistory(request):
    return render(request, 'helmdectpages/reportHistory.html')

def dataVisualization(request):
    return render(request, 'helmdectpages/dataVisualization.html')

def detailedReports(request):
    return render(request, 'helmdectpages/detailedReports.html')

def settings(request):
    return render(request, 'helmdectpages/settings.html')