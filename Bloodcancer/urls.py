"""
URL configuration for Bloodcancer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from BloodApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("index/", views.index),
    path("login/", views.signin),
    path("patientReg/", views.patientReg),
    path("doctorReg/", views.doctorReg),
    path("adminHome/", views.adminHome),
    path("userhome/", views.userHome),
    path("viewPatients/", views.viewPatients),
    path("predict/", views.predict),
    path("addhospital/", views.addHospital),
    path("updatehospital/", views.updateHospital),
    path("deletehospital/", views.deleteHospital),
    path("hospitalhome/", views.hospitalHome),
    path("deletedoctor/", views.deleteDoctor),
    path("myBookings/", views.myBookings),
    path("doctorHome/", views.doctorHome),
    path("docBookings/", views.docBookings),
]
