from django.urls import path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='login'),
    path('reportHistory/', views.reportHistory, name='reportHistory'),
    path('dataVisualization/', views.dataVisualization, name='dataVisualization'),
    path('detailedReports/', views.detailedReports, name='detailedReports'),
    path('settings/', views.settings, name='settings'),
]
