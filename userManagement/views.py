from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from bson.objectid import ObjectId
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage

from .models import feedback, UserProfile, Guru, Siswa, Kelas
from django.contrib.auth.models import User

import hashlib
import io
import os
import csv
# import pymongo
import json
# from bson import ObjectId

# from django.conf import settings
# my_client = pymongo.MongoClient(settings.DB_NAME)
# dbname = my_client['datasiswa'] # Nama Database
# userDetail = dbname["users"] # Nama Tabel
# userLogin = dbname["login"] # Nama Tabel
# categoryDb = dbname["category"]
# feedbackdb = dbname["feedback"]


# Custom JSON encoder class to handle ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


# Create your views here.
def checkAuthentication(r):
    if not r.user.is_authenticated:
        return redirect('login')
    role =  r.session.get('role')
    if role != "ADMIN":
        return True
    return False

def index(request):
    if checkAuthentication(request):
        return redirect('index')
    allUser = UserProfile.objects.select_related('user','guru','siswa','siswa__id_kelas').all()
    return render(request, 'users/index.html',{'data': allUser})

def addUser(request):
    if checkAuthentication(request):
        return redirect('index')
    allKelas = Kelas.objects.all()
    return render(request, 'users/addUser.html',{'kelasAll':allKelas})

def editUser(request,user_id):
    if checkAuthentication(request):
        return redirect('index')
    user = UserProfile.objects.select_related('user','guru','siswa','siswa__id_kelas').get(id=user_id)
    allKelas = Kelas.objects.all()
    return render(request, 'users/editUser.html',{'userDetails':user,'kelasAll':allKelas})

def deleteUser(request,user_id):
    userProfile = UserProfile.objects.get(id=user_id)
    if userProfile.user:
        userAuth = User.objects.get(id=userProfile.user.id)
        userAuth.delete()
    else:
        userProfile.delete()
    return redirect('userManagementIndex')

def createUser(request):
    if request.FILES.get('profile-pic'):
        pic_name = profilePicHandler(request)
    else:
        pic_name = 'default.jpeg'

    new_user_profile = UserProfile(
        nama_Lengkap=request.POST['name'],
        jenis_kelamin='L' if request.POST['kelamin'] == 'Laki-Laki' else 'P',
        tempat_lahir=request.POST['tempat-lahir'],
        tanggal_lahir=request.POST['tanggal-lahir'],
        alamat=request.POST['alamat'],
        no_hp=request.POST['phone'],
        role=request.POST['role'],
        pic=pic_name
    )
    new_user_profile.save()
    if not request.POST['username'] == "":
        new_user = User.objects.create_user(request.POST['username'], request.POST['password'])
        new_user_profile.user = new_user
        new_user_profile.save()

    if request.POST['role'] == 'GURU':
        new_guru = Guru(
            user_profile=new_user_profile,
            nip=request.POST['nip'],
            bidang_studi=request.POST['bidang_studi']
        )
        new_guru.save()

    elif request.POST['role'] == 'SISWA':
        try:
            if request.POST['kelas'] != "None":
                curr_kelas = Kelas.objects.get(unique_id=request.POST['kelas'])
        except:
            tingkat=request.POST['kelas'].split('-')[0]
            grup=request.POST['kelas'].split('-')[1]
            newKelas = Kelas(
                unique_id=request.POST['kelas'],
                tingkat=tingkat,
                grup=grup
            )
            newKelas.save()

        new_siswa = Siswa(
            user_profile=new_user_profile,
            id_kelas=Kelas.objects.get(unique_id=request.POST['kelas']),
            nis=request.POST['nis'],
            nisn=request.POST['nisn'],
            angkatan=request.POST['angkatan'],            
        )
        new_siswa.save()

    return redirect('userManagementIndex')

def profilePicHandler(request):
    uploaded_file = request.FILES['profile-pic']
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
    uploaded_file.name = hashed_file_name
    default_storage.save("static/profilePic/"+uploaded_file.name, uploaded_file)
    return uploaded_file.name    

def updateUser(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)

    # Update the UserProfile fields with the provided data
    user_profile.nama_Lengkap = request.POST['name']
    user_profile.jenis_kelamin = 'L' if request.POST['kelamin'] == 'Laki-Laki' else 'P'
    user_profile.tempat_lahir = request.POST['tempat-lahir']
    user_profile.tanggal_lahir = request.POST['tanggal-lahir']
    user_profile.alamat = request.POST['alamat']
    user_profile.no_hp = request.POST['phone']
    if user_profile.role != request.POST['role']:
        if user_profile.role == "SISWA":
            siswa = Siswa.objects.get(user_profile=user_profile)
            siswa.delete()
        elif user_profile.role == "GURU":
            guru = Guru.objects.get(user_profile=user_profile)
            guru.delete()
        user_profile.role = request.POST['role']

    if request.FILES.get('profile-pic'):
        pic_name = profilePicHandler(request)
    else:
        pic_name = user_profile.pic
    user_profile.pic = pic_name
    if user_profile.user and request.POST['username'] != "":
        userAuth = User.objects.get(username=user_profile.user.username)
        if user_profile.user.username != request.POST['username']:
            userAuth.user.username = new_username
            userAuth.user.save()
        # db_login.update_one({"_idUser":ObjectId(user_id)},{'$set':{'username':request.POST['username']}})
        if request.POST['password'] != "":
            userAuth.user.set_password(request.POST['password'])
            userAuth.user.save()
    else:
        user_profile.user = User.objects.create_user(request.POST['username'], request.POST['password'])
    user_profile.save()

    if request.POST['role'] == 'GURU':
        try:
            guru = Guru.objects.get(user_profile=user_profile)
            guru.nip = request.POST['nip']
            guru.bidang_studi=request.POST['bidang_studi']
            guru.save()
        except:
            new_guru = Guru(
                user_profile=user_profile,
                nip=request.POST['nip'],
                bidang_studi=request.POST['bidang_studi'])
            new_guru.save()
    elif request.POST['role'] == 'SISWA':
        try:
            if request.POST['kelas'] != "None":
                curr_kelas = Kelas.objects.get(unique_id=request.POST['kelas'])
        except:
            tingkat=request.POST['kelas'].split('-')[0]
            grup=request.POST['kelas'].split('-')[1]
            newKelas = Kelas(
                unique_id=request.POST['kelas'],
                tingkat=tingkat,
                grup=grup
            )
            newKelas.save()
        try:
            siswa = Siswa.objects.get(user_profile=user_profile)
            siswa.id_kelas=Kelas.objects.get(unique_id=request.POST['kelas'])
            siswa.nis=request.POST['nis']
            siswa.nisn=request.POST['nisn']
            angkatan=request.POST['angkatan']
            siswa.save()
        except:
            new_siswa = Siswa(
                user_profile=user_profile,
                id_kelas=Kelas.objects.get(unique_id=request.POST['kelas']),
                nis=request.POST['nis'],
                nisn=request.POST['nisn'],
                angkatan=request.POST['angkatan'],            
            )
            new_siswa.save()

    return redirect('userManagementIndex')

def userFeedback(request):
    if checkAuthentication(request):
        return redirect('index')
    all_feedback = feedback.objects.select_related('user_profile').all()
    print(all_feedback)
    return render(request, 'users/userFeedback.html',{'data': all_feedback})

def deleteFeedback(request,feedback_id):
    fb = feedback.objects.get(id=feedback_id)
    fb.delete()
    return redirect('userFeedback')    

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
