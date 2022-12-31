from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

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
    loggedIn = request.session.get('login')
    if not loggedIn:
        return redirect('login')
    user_details = db_users.find()
    data = {
        'users' : user_details,
    }
    return render(request, 'index.html',data)

def login(request):
    loggedIn = request.session.get('login')
    if loggedIn:
        return redirect('home')
    return render(request, 'login.html')

def authenticate(request):
    data = {
        "username":request.POST['username']
    }
    result = db_login.find_one(data)
    if result is None:
        return redirect('login')
    print(result)
    if not check_password(request.POST['password'],result['password']):
        return redirect('login')
    request.session['login'] = True
    request.session['username'] = request.POST['username']
    return redirect('home')

def logout(request):
    request.session.clear()
    return redirect('login')