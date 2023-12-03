from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='userManagementIndex'),
    path('/users/add',views.addUser,name='addUser'),
    path('/users/add/new',views.createUser,name='newUser'),
    path('/users/edit/<str:user_id>', views.editUser, name="editUser"),
    path('/users/edit/<str:user_id>/update', views.updateUser, name="updateUser"),
    path('/users/delete/<str:user_id>', views.deleteUser, name="deleteUser"),
    path('/users/feedback',views.userFeedback,name='userFeedback'),
    path('/users/feedback/<str:feedback_id>/delete',views.deleteFeedback,name='deleteFeedback'),
    path('/users/export/userdata',views.exportCSV,name='exportcsv'),
    path('/users/import/userdata',views.importCSV,name='importcsv'),
    path('/users/import/userdata',views.importCSV,name='importcsv'),
    # path('/users/category/add',views.addCategory,name='addCategory'),
    # path('/users/category/add/new',views.newCategory,name='newCategory'),
    # path('/users/category/edit', views.editCategory, name="editCategory"),
    # path('/users/category/edit/update/<str:category_id>', views.updateCategory, name="updateCategory"),
    # path('/users/category/delete/<str:category_id>', views.deleteCategory, name="deleteCategory"),

    ] 