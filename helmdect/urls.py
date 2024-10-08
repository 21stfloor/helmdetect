"""
URL configuration for helmdect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from helmdectpages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('test-firebase/', views.test_database, name='test_firebase'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),
    # path('home/', views.home, name='home'),
    path('report_history/', views.report_history, name='report_history'),
    path('detailed-reports/', views.detailed_reports, name='detailed_reports'),
    path('settings/', views.settings, name='settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('process_image/', views.process_image, name='process_image')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
