from django.urls import path
from . import views
urlpatterns = [
    path('', views.register, name='register'),
    # path('test-firebase/', views.test_database, name='test_firebase'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('report-history/', views.report_history, name='report_history'),
    path('data-visualization/', views.data_visualization, name='data_visualization'),
    path('detailed-reports/', views.detailed_reports, name='detailed_reports'),
    path('settings/', views.settings, name='settings'),
]
