from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='absensiIndex'),
    path('/add',views.addAbsensi,name='addAbsensi'),
    path('/add/new',views.createAbsensi,name='createAbsensi'),
    path('/update',views.updateAbsensi,name='updateAbsensi'),
    path('/delete/<str:idAbsensi>',views.deleteAbsensi,name='deleteAbsensi'),
    path('/edit/<str:idAbsensi>',views.editAbsensi,name='editAbsensi'),

    ]