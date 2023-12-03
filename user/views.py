from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password
from userManagement.models import feedback, UserProfile


# from bson.objectid import ObjectId

# import pymongo
from django.conf import settings

# my_client = pymongo.MongoClient(settings.DB_NAME)

# dbname = my_client['datasiswa'] # Nama Database
# db_users = dbname["users"] # Nama Tabel
# db_login = dbname['login']
# db_feedback = dbname['feedback']


# Create your views here.
def feedback_view(request):
    return render(request, 'users/feedback.html')

def postFeedback(request):
    user_profile = UserProfile.objects.get(user=request.user)
    newFeedback = feedback(user_profile=user_profile, feedback=request.POST['feedback'])
    newFeedback.save()
    return redirect("home")