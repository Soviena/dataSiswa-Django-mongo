from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('users/add/',views.addUser,name='addUser'),
    path('users/add/new',views.createUser,name='newUser'),
    path('users/edit/<str:user_id>', views.editUser, name="editUser"),
    path('users/delete/<str:user_id>', views.deleteUser, name="deleteUser")
    ]