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
def isLogin(r):
    return r.session.get('login')
def getRole(r):
    role =  r.session.get('role')
    return role

def index(request):
    if not isLogin(request):
        return redirect('login')
    role = getRole(request)
    if role == "ADMIN":
        return redirect('home')
    else:
        return redirect('user')

def home(request):
    return render(request, 'home.html')

def login(request):
    if isLogin(request):
        return redirect('home')
    return render(request, 'login.html')

def authenticate(request):
    data = {
        "username":request.POST['username']
    }
    result = db_login.find_one(data)
    if result is None:
        return redirect('login')
    if not check_password(request.POST['password'],result['password']):
        return redirect('login')
    request.session['login'] = True
    request.session['username'] = request.POST['username']
    request.session['role'] = result['role']
    request.session['uid'] = str(result['_id'])
    return redirect('home')

def logout(request):
    request.session.clear()
    return redirect('login')