from django.urls import path

from . import views

urlpatterns = [
    path('/feedback',views.feedback, name='feedback'),
    path('/feedback/post',views.postFeedback, name='postFeedback'),
    ]