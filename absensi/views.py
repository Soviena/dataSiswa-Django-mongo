from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password

from bson.objectid import ObjectId

import pymongo
from django.conf import settings

my_client = pymongo.MongoClient(settings.DB_NAME)

dbname = my_client['datasiswa'] # Nama Database
db_users = dbname["users"] # Nama Tabel
db_login = dbname['login']


# Create your views here.
def index(request):
    return render(request, 'users/absensi.html')
