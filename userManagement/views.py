from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from bson.objectid import ObjectId
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
import hashlib
import io
import os
import csv
import pymongo
import json
from bson import ObjectId

from django.conf import settings
my_client = pymongo.MongoClient(settings.DB_NAME)
dbname = my_client['datasiswa'] # Nama Database
userDetail = dbname["users"] # Nama Tabel
userLogin = dbname["login"] # Nama Tabel
categoryDb = dbname["category"]

# Custom JSON encoder class to handle ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


# Create your views here.
def checkAuthentication(r):
    role =  r.session.get('role')
    print(role)
    if role != "ADMIN":
        return True
    return False

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
    categoryList = categoryDb.find()
    categoryJson = json.dumps([document for document in categoryDb.find()],cls=JSONEncoder)
    return render(request, 'users/addUser.html',{"categoryList":categoryList,"categoryJSON":categoryJson})

def addCategory(request):
    return render(request, 'users/addCategory.html')

def editCategory(request):
    categoryList = categoryDb.find()
    categoryJson = json.dumps([document for document in categoryDb.find()],cls=JSONEncoder)
    return render(request, 'users/editCategory.html',{"categoryList":categoryList,"categoryJSON":categoryJson})

def updateCategory(request, category_id):
    data = {'$set':{ 
        "template" : request.POST.getlist('key')
    }}
    categoryDb.update_one({"_id": ObjectId(category_id)},data) 
    return redirect('editCategory')

def deleteCategory(request, category_id):
    categoryDb.delete_one({"_id": ObjectId(category_id)})
    return redirect('editCategory')


def newCategory(request):
    data = {
        "name" : request.POST["name"],
        "template" : request.POST.getlist('key')
    }
    categoryDb.insert_one(data)
    return redirect('addUser')
    
def editUser(request,user_id):
    categoryList = categoryDb.find()
    categoryJson = json.dumps([document for document in categoryDb.find()],cls=JSONEncoder)    
    user_details = userDetail.find_one({"_id": ObjectId(user_id)})
    user_login = userLogin.find_one({"_idUser": ObjectId(user_id)})
    return render(request, 'users/editUser.html',{'userDetails':user_details,'userLogin':user_login, "categoryList":categoryList,"categoryJSON":categoryJson})

def deleteUser(request,user_id):
    userDetail.delete_one({"_id": ObjectId(user_id)})
    userLogin.delete_one({"_idUser": ObjectId(user_id)})
    return redirect('userManagementIndex')

def createUser(request):
    data = {
    "nama_Lengkap" : request.POST['name'],
    "jenis_kelamin" : request.POST['kelamin'],
    "tempat_lahir" : request.POST['tempat-lahir'],
    "tanggal_lahir" : request.POST['tanggal-lahir'],
    "alamat": request.POST['alamat'],
    "no_hp": request.POST['phone'],
    "userData" : dict(zip(request.POST.getlist('key'),request.POST.getlist('value')))
    }
    ids = userDetail.insert_one(data)
    if not request.POST['username'] == "":
        createLogin(request, ids.inserted_id)
    return redirect('userManagementIndex')

def profilePicHandler(request, update=False):
    uploaded_file = request.FILES['profile-pic']
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
    uploaded_file.name = hashed_file_name
    default_storage.save("static/profilePic/"+uploaded_file.name, uploaded_file)
    if update:
        userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'profilePic':uploaded_file.name}})
        return
    return uploaded_file.name    


def createLogin(request, userid, update=False):
    if request.POST['username'] == "":
        return
    data = {
        "_idUser" : userid,
        "username": request.POST['username'],
        "password": make_password(request.POST['password']),
        "role": request.POST['role']
    }
    if request.FILES.get('profile-pic'):
        data['profilePic'] = profilePicHandler(request)
    userLogin.insert_one(data)

def updateUser(request, user_id):
    data = {
        "nama_Lengkap" : request.POST['name'],
        "jenis_kelamin" : request.POST['kelamin'],
        "tempat_lahir" : request.POST['tempat-lahir'],
        "tanggal_lahir" : request.POST['tanggal-lahir'],
        "alamat": request.POST['alamat'],
        "no_hp": request.POST['phone'],
        "userData" : dict(zip(request.POST.getlist('key'),request.POST.getlist('value')))
    }
    userDetail.replace_one({"_id": ObjectId(user_id)},data)
    if userLogin.find_one({"_idUser":ObjectId(user_id)}) is None:
        createLogin(request, ObjectId(user_id))
    else:
        userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'username':request.POST['username']}})
        userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'role':request.POST['role']}})
        if request.POST['password'] != "":
            userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'password':make_password(request.POST['password'])}})
    if request.FILES.get('profile-pic'):
        profilePicHandler(request, True)
        
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

def exportCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    cursor = dbname.users.aggregate([
        {
            '$lookup': {
                'from': 'login',
                'localField': '_id',
                'foreignField': '_idUser',
                'as': 'userLogin'
            }
        }
    ])
    data = [doc for doc in cursor]
    # Create the CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['_id','nama_Lengkap', 'jenis_kelamin', 'tempat_lahir','tanggal_lahir','alamat','no_hp','_idLogin','_idUser','username','role','password','userData'])
    for doc in data:         
        if len(doc['userLogin']) == 0:
            doc['userLogin'].append({})
        writer.writerow([
            doc['_id'],doc['nama_Lengkap'], doc['jenis_kelamin'], doc['tempat_lahir'],doc['tanggal_lahir'],doc['alamat'],doc['no_hp'],
            doc['userLogin'][0].get('_id'),doc['userLogin'][0].get('_idUser'),doc['userLogin'][0].get('username'),doc['userLogin'][0].get('role'),doc['userLogin'][0].get('password'),
            doc['userData']])

    return response

def importCSV(request):
    # Get the uploaded file
    uploaded_file = request.FILES['csv']

        # Use the csv module to read the file
    csv_file = io.TextIOWrapper(uploaded_file, encoding='utf-8')
    reader = csv.DictReader(csv_file)

    # Process the rows in the file
    for row in reader:
        data = {
            "nama_Lengkap" : row['nama_Lengkap'],
            "jenis_kelamin" : row['jenis_kelamin'],
            "tempat_lahir" : row['tempat_lahir'],
            "tanggal_lahir" : row['tanggal_lahir'],
            "alamat": row['alamat'],
            "no_hp": row['no_hp'],
            "userData" : json.loads(row['userData'].replace("'", '"'))
        }
        userDetail.replace_one({"_id": ObjectId(row['_id'])},data,upsert=True)
        if row['_idLogin'] not in ["None",'']:
            dataLogin = {
                "_idUser" : ObjectId(row['_idUser']),
                "username": row['username'],
                "password": row['password'],
                "role":row['role']
            }
            userLogin.replace_one({"_id":ObjectId(row['_idLogin'])},dataLogin,upsert=True)


    # Delete the file when you're done with it
    csv_file.close()
    del uploaded_file

    # Redirect to a success page
    return redirect('userManagementIndex')
