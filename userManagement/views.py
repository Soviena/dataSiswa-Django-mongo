from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from bson.objectid import ObjectId
import io
import csv
import pymongo
from django.conf import settings
my_client = pymongo.MongoClient(settings.DB_NAME)
dbname = my_client['datasiswa'] # Nama Database
userDetail = dbname["users"] # Nama Tabel
userLogin = dbname["login"] # Nama Tabel


# Create your views here.
def checkAuthentication(r):
    role =  e.session.get('role')
    if role != "ADMIN":
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
    writer.writerow(['nama_Lengkap', 'jenis_kelamin', 'tempat_lahir','tanggal_lahir','alamat','no_hp','_idUser','username','role','password'])
    for doc in data:
        if len(doc['userLogin']) >= 1:
            writer.writerow([doc['nama_Lengkap'], doc['jenis_kelamin'], doc['tempat_lahir'],doc['tanggal_lahir'],doc['alamat'],doc['no_hp'],doc['userLogin'][0]['_idUser'],doc['userLogin'][0]['username'],doc['userLogin'][0]['role'],doc['userLogin'][0]['password']])
        else:
            writer.writerow([doc['nama_Lengkap'], doc['jenis_kelamin'], doc['tempat_lahir'],doc['tanggal_lahir'],doc['alamat'],doc['no_hp']])

    return response

def importCSV(request):
        # Get the uploaded file
        uploaded_file = request.FILES['csv']

         # Use the csv module to read the file
        csv_file = io.TextIOWrapper(uploaded_file, encoding='utf-8')
        reader = csv.DictReader(csv_file)

        # Process the rows in the file
        for row in reader:
            print(row)


        # Delete the file when you're done with it
        csv_file.close()
        del uploaded_file

        # Redirect to a success page
        return redirect('userManagementIndex')
