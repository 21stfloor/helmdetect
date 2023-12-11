from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register, name='register'),
    # path('test-firebase/', views.test_database, name='test_firebase'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('report-history/', views.report_history, name='report_history'),
    path('data-visualization/', views.data_visualization, name='data_visualization'),
    path('detailed-reports/', views.detailed_reports, name='detailed_reports'),
    path('settings/', views.settings, name='settings'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)