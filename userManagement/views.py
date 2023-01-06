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
userDetail = dbname["users"] # Nama Tabel
userLogin = dbname["login"] # Nama Tabel


# Create your views here.
def checkAuthentication(r):
    role =  e.session.get('role')
    if role is not "ADMIN":
        return redirect('index')
    return

def index(request):
    cursor = dbname.users.aggregate([
        {
            '$lookup': {
                'from': 'login',
                'localField': '_id',
                'foreignField': '_idUser',
                'as': 'userInfo'
            }
        }
    ])
    data = [doc for doc in cursor]
    return render(request, 'users/index.html',{'data': data})

def addUser(request):
    return render(request, 'users/addUser.html')

def editUser(request,user_id):
    cursor = dbname.users.aggregate([
        {
            '$lookup': {
                'from': 'login',
                'localField': '_id',
                'foreignField': '_idUser',
                'as': 'userInfo'
            }
        }
    ])
    data = [doc for doc in cursor]
    return render(request, 'users/editUser.html',{'user':data})

def deleteUser(request,user_id):
    userDetail.delete_one({"_id": ObjectId(user_id)})
    return redirect('userManagementIndex')

def createUser(request):
    data = {
    "nama_Lengkap" : request.POST['name'],
    "jenis_kelamin" : request.POST['kelamin'],
    "tempat_lahir" : request.POST['tempat-lahir'],
    "tanggal_lahir" : request.POST['tanggal-lahir'],
    "alamat": request.POST['alamat'],
    "no_hp": request.POST['phone']
    }
    ids = userDetail.insert_one(data)
    if not request.POST['username'] == "":
        data = {
            "_idUser" : ids.inserted_id,
            "username": request.POST['username'],
            "password": make_password(request.POST['password']),
            "role": request.POST['role']
        }
        userLogin.insert_one(data)
    return redirect('userManagementIndex')

def updateUser(request, user_id):
    data = {
    "nama_Lengkap" : request.POST['name'],
    "jenis_kelamin" : request.POST['kelamin'],
    "tempat_lahir" : request.POST['tempat-lahir'],
    "tanggal_lahir" : request.POST['tanggal-lahir'],
    "alamat": request.POST['alamat'],
    "no_hp": request.POST['phone']
    }
    userDetail.replace_one({"_id": ObjectId(user_id)},data)
    userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'username':request.POST['username']}})
    userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'role':request.POST['role']}})
    if request.POST['password'] != "":
        userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'password':make_password(request.POST['username'])}})
        
    return redirect('userManagementIndex')

def userFeedback(request):
    cursor = dbname.feedback.aggregate([
        {
            '$lookup': {
                'from': 'login',
                'localField': '_idUser',
                'foreignField': '_id',
                'as': 'userDetail'
            }
        }
    ])
    data = [doc for doc in cursor]
    return render(request, 'users/userFeedback.html',{'data': data})