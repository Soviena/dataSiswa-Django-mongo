from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password

from bson.objectid import ObjectId

import pymongo, json
from django.conf import settings
from bson import ObjectId
from datetime import datetime

my_client = pymongo.MongoClient(settings.DB_NAME)

dbname = my_client['datasiswa'] # Nama Database
db_users = dbname["users"] # Nama Tabel
dbKelas = dbname['kelas']
dbAbsensi = dbname['absensi']

access = ["GURU","ADMIN"]

def checkAuthentication(r):
    role =  r.session.get('role')
    if role not in access:
        return True
    return False


def index(request):
    if checkAuthentication(request):
        return redirect('index')
    data = dbAbsensi.find()
    data = [doc for doc in data]
    return render(request, 'absensi/index.html',{'data': data})

def addAbsensi(request):
    if checkAuthentication(request):
        return redirect('index')    
    user_details = db_users.find_one({"_id":  ObjectId(request.session['uids'])})
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
    return render(request, 'absensi/absensi.html',{'data': data,'userLogin':user_details,'role':['GURU','STAFF','ADMIN']})

def editAbsensi(request,idAbsensi):
    if checkAuthentication(request):
        return redirect('index')
    dataAbsen = dbAbsensi.find_one({"_id": ObjectId(idAbsensi)})
    return render(request, 'absensi/editAbsensi.html',{'data': dataAbsen,'role':['GURU','STAFF','ADMIN']})

def createAbsensi(request):
    data = {
    "mata_pelajaran" : request.POST['mapel'],
    "nama_pengajar" : request.POST['name'],
    "id_pengajar" : request.session['uid'],
    "pertemuan" : request.POST['pertemuan'],
    "tanggal_kelas" : request.POST['tanggal-kelas'],
    "kelas": request.POST['kelas'],
    "materi": request.POST['materi'],
    "catatan" : request.POST['catatan'],
    "status" : "Disubmit",
    "waktu_submit" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "waktu_update": "-",
    "foto": "",
    "data": []
    }
    if request.FILES.get('picture'):
        data['foto'] = picHandler(request)

    siswa = []
    name = []
    nis = []
    kelas = []
    status = []
    id = []
    for key in request.POST:
        if key.startswith('idSiswa['):
            id.append(request.POST[key])
        if key.startswith('siswaName['):
            name.append(request.POST[key])
        if key.startswith('nis['):
            nis.append(request.POST[key])
        if key.startswith('kelas['):
            kelas.append(request.POST[key])
        if key.startswith('status['):
            status.append(request.POST[key])

    for name, nis, kelas, status, id in zip(name, nis, kelas, status, id):
        combined_dict = {
            'id' : id,
            'name': name,
            'nis': nis,
            'kelas': kelas,
            'status': status
        }
        siswa.append(combined_dict)
    data['data'] = siswa

    dbAbsensi.insert_one(data)

    return redirect('absensiIndex')

def updateAbsensi(request):
    data = {
    "mata_pelajaran" : request.POST['mapel'],
    "nama_pengajar" : request.POST['name'],
    "pertemuan" : request.POST['pertemuan'],
    "tanggal_kelas" : request.POST['tanggal-kelas'],
    "kelas": request.POST['kelas'],
    "materi": request.POST['materi'],
    "catatan" : request.POST['catatan'],
    "status" : "Disubmit, Diupdate",
    "waktu_submit" : request.POST['submit-time'],
    "waktu_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "foto": "",
    "data": []
    }
    if request.FILES.get('picture'):
        data['foto'] = picHandler(request)

    siswa = []
    name = []
    nis = []
    kelas = []
    status = []
    id = []
    for key in request.POST:
        if key.startswith('idSiswa['):
            id.append(request.POST[key])
        if key.startswith('siswaName['):
            name.append(request.POST[key])
        if key.startswith('nis['):
            nis.append(request.POST[key])
        if key.startswith('kelas['):
            kelas.append(request.POST[key])
        if key.startswith('status['):
            status.append(request.POST[key])

    for name, nis, kelas, status, id in zip(name, nis, kelas, status, id):
        combined_dict = {
            'id' : id,
            'name': name,
            'nis': nis,
            'kelas': kelas,
            'status': status
        }
        siswa.append(combined_dict)
    data['data'] = siswa

    dbAbsensi.replace_one({"_id": ObjectId(request.POST['id'])},data)

    return redirect('absensiIndex')

def deleteAbsensi(request, idAbsensi):
    dbAbsensi.delete_one({"_id": ObjectId(idAbsensi)})
    return redirect('absensiIndex')

def picHandler(request, update=False):
    uploaded_file = request.FILES['picture']
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
    uploaded_file.name = hashed_file_name
    default_storage.save("static/absensi/"+uploaded_file.name, uploaded_file)
    # if update:
    #     userLogin.update_one({"_idUser":ObjectId(user_id)},{'$set':{'profilePic':uploaded_file.name}})
    #     return
    return uploaded_file.name