from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='penilaianIndex'),
    path('/addMatpel',views.addMatpel, name='addMatpel'),
    path('/addKomponen',views.addKomponen, name='addKomponen'),
    path('/deleteKomponen/<str:idKomponen>',views.hapusKomponen,name='deleteKomponen'),
    path('/nilai/add',views.inputNilai, name='addNilai'),
    path('/nilai/<str:idKomponen>',views.nilaiSiswa, name='nilaiSiswa'),


    ] 