from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password

from userManagement.models import feedback, UserProfile, Guru, Siswa, Kelas, Absensi, AbsensiSiswa, Pelajaran
from django.db.models import Prefetch

# from bson.objectid import ObjectId

# import pymongo, json
from django.conf import settings
# from bson import ObjectId
from datetime import datetime

# my_client = pymongo.MongoClient(settings.DB_NAME)

# dbname = my_client['datasiswa'] # Nama Database
# db_users = dbname["users"] # Nama Tabel
# dbKelas = dbname['kelas']
# dbAbsensi = dbname['absensi']

access = ["GURU","ADMIN"]

def checkAuthentication(r):
    if not r.user.is_authenticated:
        return redirect('login')
    if r.session.get('role') not in access:
        return redirect('index')

def index(request):
    checkAuthentication(request)
    absensi_siswa_prefetch = Prefetch(
        'absensisiswa_set',
        queryset=AbsensiSiswa.objects.select_related('id_siswa__user_profile__user'),
        to_attr='siswa_absensi_list'
    )
    data = Absensi.objects.prefetch_related(absensi_siswa_prefetch).all()
    return render(request, 'absensi/index.html',{'data': data})

def addAbsensi(request):
    checkAuthentication(request)
    current_user = UserProfile.objects.select_related('user').get(user=request.user)
    allSiswa = Siswa.objects.select_related('id_kelas','user_profile').all()
    allKelas = Kelas.objects.all()
    allMatpel = Pelajaran.objects.all()
    return render(request, 'absensi/absensi.html',{'data': allSiswa,'allKelas':allKelas,'userLogin':current_user,'allMatpel':allMatpel})

def editAbsensi(request,idAbsensi):
    checkAuthentication(request)
    current_user = UserProfile.objects.select_related('user').get(user=request.user)
    allSiswa = Siswa.objects.select_related('id_kelas','user_profile').all()
    allKelas = Kelas.objects.all()
    allMatpel = Pelajaran.objects.all()
    absensi_siswa_prefetch = Prefetch(
        'absensisiswa_set',
        queryset=AbsensiSiswa.objects.select_related('id_siswa__user_profile__user'),
        to_attr='siswa_absensi_list'
    )
    dataAbsen = Absensi.objects.prefetch_related(absensi_siswa_prefetch).get(id=idAbsensi)
    return render(request, 'absensi/editAbsensi.html',{'data': dataAbsen,'allKelas':allKelas,'userLogin':current_user,'allMatpel':allMatpel})

def createAbsensi(request):
    # try:
    matpel = Pelajaran.objects.get(singkatan=request.POST['matpel'])
    # except:
    #     matpel = Pelajaran(
    #         nama=request.POST['matpel'].split('-')[1],
    #         singkatan=request.POST['matpel'].split('-')[0]
    #     )
    #     matpel.save()
    if request.FILES.get('picture'):
        picName = picHandler(request)
    else:
        picName = ""
    newAbsensi = Absensi(
        materi=request.POST['materi'],
        catatan=request.POST['catatan'],
        tanggal=request.POST['tanggal-kelas'],
        pertemuan=request.POST['pertemuan'],
        id_pelajaran=matpel,
        id_kelas=Kelas.objects.get(unique_id=request.POST['kelas']),
        id_user=request.user,
        pic=picName
    )
    newAbsensi.save()
    siswaList = []
    statusList = []
    for key in request.POST:
        if key.startswith('idSiswa['):
            siswaList.append(request.POST[key])
        if key.startswith('status['):
            statusList.append(request.POST[key])
    for i in range(len(siswaList)):
        currSiswa = Siswa.objects.get(id=siswaList[i])
        currKeterangan = statusList[i]
        currSiswa.absensi.add(newAbsensi, through_defaults={'keterangan':currKeterangan})

    return redirect('absensiIndex')

def updateAbsensi(request):

    absensi_siswa_prefetch = Prefetch(
        'absensisiswa_set',
        queryset=AbsensiSiswa.objects.select_related('id_siswa__user_profile__user'),
        to_attr='siswa_absensi_list'
    )
    dataAbsen = Absensi.objects.prefetch_related(absensi_siswa_prefetch).get(id=request.POST['id'])
    # try:
    matpel = Pelajaran.objects.get(singkatan=request.POST['matpel'])
    # except:
    #     matpel = Pelajaran(
    #         nama=request.POST['matpel'].split('-')[1],
    #         singkatan=request.POST['matpel'].split('-')[0]
    #     )
    #     matpel.save()
    if dataAbsen.id_pelajaran.id != matpel.id:
        dataAbsen.id_pelajaran = matpel
    if request.FILES.get('picture'):
        dataAbsen.pic = picHandler(request)
        
    dataAbsen.materi=request.POST['materi']
    dataAbsen.catatan=request.POST['catatan']
    dataAbsen.tanggal=request.POST['tanggal-kelas']
    dataAbsen.pertemuan=request.POST['pertemuan']
    dataAbsen.save()

    siswaList = []
    statusList = []
    for key in request.POST:
        if key.startswith('idSiswa['):
            siswaList.append(request.POST[key])
        if key.startswith('status['):
            statusList.append(request.POST[key])
    for i in range(len(siswaList)):
        currSiswa = Siswa.objects.get(id=siswaList[i])
        currKeterangan = statusList[i]
        currSiswa.absensi.remove(dataAbsen)
        currSiswa.absensi.add(dataAbsen, through_defaults={'keterangan':currKeterangan})

    return redirect('absensiIndex')

def deleteAbsensi(request, idAbsensi):
    absen = Absensi.objects.get(id=idAbsensi)
    absen.delete()
    return redirect('absensiIndex')

def picHandler(request, update=False):
    uploaded_file = request.FILES['picture']
    file_name, file_extension = os.path.splitext(uploaded_file.name)
    hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
    uploaded_file.name = hashed_file_name
    default_storage.save("static/absensi/"+uploaded_file.name, uploaded_file)
    return uploaded_file.name