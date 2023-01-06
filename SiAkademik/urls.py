"""SiAkademik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.staticfiles.urls import static

from .settings import STATIC_URL
from .settings import STATIC_ROOT
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('login',views.login,name='login'),
    path('login/authenticate', views.authenticate,name="auth"),
    path('logout', views.logout,name="logout"),
    path('userManagement/',include('userManagement.urls')),
    path('user/',include('user.urls'))
] + static(STATIC_URL, document_root=STATIC_ROOT)
