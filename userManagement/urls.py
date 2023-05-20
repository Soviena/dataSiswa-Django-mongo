from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='userManagementIndex'),
    path('users/add/',views.addUser,name='addUser'),
    path('users/add/new',views.createUser,name='newUser'),
    path('users/edit/<str:user_id>', views.editUser, name="editUser"),
    path('users/edit/<str:user_id>/update', views.updateUser, name="updateUser"),
    path('users/delete/<str:user_id>', views.deleteUser, name="deleteUser"),
    path('users/feedback/',views.userFeedback,name='userFeedback'),
    path('users/export/userdata/',views.exportCSV,name='exportcsv'),
    path('users/import/userdata/',views.importCSV,name='importcsv'),
    path('users/import/userdata/',views.importCSV,name='importcsv'),
    path('users/category/add/',views.addCategory,name='addCategory'),
    path('users/category/add/new',views.newCategory,name='newCategory'),
    ] 