from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from bson.objectid import ObjectId

import pymongo
from django.conf import settings
my_client = pymongo.MongoClient(settings.DB_NAME)
dbname = my_client['datasiswa'] # Nama Database
collection_name = dbname["users"] # Nama Tabel

# Create your views here.
def index(request):
    user_details = collection_name.find()
    data = {
        'users' : user_details,
    }
    return render(request, 'users/index.html',data)

def addUser(request):
    return render(request, 'users/addUser.html')

def editUser(request,user_id):
    user_details = collection_name.find_one({"_id": ObjectId(user_id)})
    data = {
        'user':user_details
    }
    return render(request, 'users/editUser.html',data)

def deleteUser(request,user_id):
    user_details = collection_name.delete_one({"_id": ObjectId(user_id)})
    return redirect('index')

def createUser(request):
    data = {
    "nama_Lengkap" : request.POST['name'],
    "jenis_kelamin" : request.POST['kelamin'],
    "tempat_lahir" : request.POST['tempat-lahir'],
    "tanggal_lahir" : request.POST['tanggal-lahir'],
    "alamat": request.POST['alamat'],
    "no_hp": request.POST['phone']
    }
    collection_name.insert_one(data)
    return redirect('index')