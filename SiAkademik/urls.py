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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('login',views.login_page,name='login'),
    path('login/authenticate', views.auth,name="auth"),
    path('logout', views.logout_fun,name="logout"),
    path('profile/view/<str:username>', views.profile, name="profile"),
    path('profile/edit', views.profileEdit, name="profileEdit"),
    path('profile/update', views.profileUpdate, name="profileUpdate"),
    path('userManagement',include('userManagement.urls')),
    path('user',include('user.urls')),
    path('absensi',include('absensi.urls')),
    path('admin/', admin.site.urls),
    path('penilaian', include('penilaian.urls')),

]
urlpatterns += staticfiles_urlpatterns()
