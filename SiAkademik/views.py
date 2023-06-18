from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.files.storage import default_storage

from django.contrib.auth.hashers import make_password, check_password

from bson.objectid import ObjectId

import os
import hashlib
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

    return redirect('home')

def home(request):
    if not isLogin(request):
        return redirect('login')
    role = getRole(request)
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
    request.session['uids'] = str(result['_idUser'])
    request.session['pic'] = "profilePic/"+str(result.get('profilePic'))

    return redirect('home')

def logout(request):
    request.session.clear()
    return redirect('login')

def profile(request,username):
    user_login = db_login.find_one({"username": username})
    user_login['profilePic'] = "profilePic/"+str(user_login.get('profilePic'))
    user_details = db_users.find_one({"_id": ObjectId(user_login.get('_idUser'))})

    return render(request, 'profile.html', {'userDetails':user_details,'userLogin':user_login})

def profileEdit(request):
    user_login = db_login.find_one({"_id": ObjectId(request.session['uid'])})
    user_details = db_users.find_one({"_id": ObjectId(user_login.get('_idUser'))})
    return render(request, 'profileEdit.html', {'userDetails':user_details,'userLogin':user_login})

def profileUpdate(request):
    loginData = db_login.find_one({"_id": ObjectId(request.session['uid'])})
    user_id = loginData['_idUser']
    userData = db_users.find_one({"_id" : ObjectId(user_id)})
    data = {
        "nama_Lengkap" : request.POST['name'],
        "jenis_kelamin" : request.POST['kelamin'],
        "tempat_lahir" : request.POST['tempat-lahir'],
        "tanggal_lahir" : request.POST['tanggal-lahir'],
        "alamat": request.POST['alamat'],
        "no_hp": request.POST['phone']
    }
    db_users.replace_one({"_id": ObjectId(userData['_id'])},data)
    if request.FILES.get('profile-pic'):
        uploaded_file = request.FILES['profile-pic']
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
        uploaded_file.name = hashed_file_name
        default_storage.save("static/profilePic/"+uploaded_file.name, uploaded_file)
        db_login.update_one({"_idUser":ObjectId(user_id)},{'$set':{'profilePic':uploaded_file.name}})
    db_login.update_one({"_idUser":ObjectId(user_id)},{'$set':{'username':request.POST['username']}})
    if request.POST['password'] != "":
        db_login.update_one({"_idUser":ObjectId(user_id)},{'$set':{'password':make_password(request.POST['username'])}})
    request.session['pic'] = "profilePic/"+str(uploaded_file.name)
    return redirect('profile',request.POST['username'])