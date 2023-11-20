from django.urls import path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('report_history/', views.report_history, name='report_history'),
    path('data_visualization/', views.data_visualization, name='data_visualization'),
    path('detailed_reports/', views.detailed_reports, name='detailed_reports'),
    path('settings/', views.settings, name='settings'),
]
