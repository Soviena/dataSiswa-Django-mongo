from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from django.core.serializers import serialize
from django.db.models import Prefetch


# Create your views here.
from userManagement.models import feedback, UserProfile, Guru, Siswa, Kelas, Absensi, AbsensiSiswa, Pelajaran, KomponenPenilaian, Nilai

access = ["GURU","ADMIN"]

def checkAuthentication(r):
    if not r.user.is_authenticated:
        return redirect('login')
    if r.session.get('role') not in access:
        return redirect('index')


def index(request):
    checkAuthentication(request)
    allMatpel = Pelajaran.objects.prefetch_related('komponenpenilaian_set').all()
    tahun_list = KomponenPenilaian.objects.values('tahun').distinct()
    tahun_list = sorted(tahun_list, key=lambda x: x['tahun'], reverse=True)
    return render(request, 'penilaian/index_penilaian.html', {'allMatpel':allMatpel,'allTahun':tahun_list})

def addMatpel(request):
    matpel = Pelajaran(
        nama=request.POST['name'],
        singkatan=request.POST['singkatan']
    )
    matpel.save()
    return redirect('penilaianIndex')

def addKomponen(request):
    komponen = KomponenPenilaian(
        pelajaran = Pelajaran.objects.get(singkatan=request.POST['pelajaran']),
        nama = request.POST['name'],
        tahun = request.POST['tahun'],
        bobot = request.POST['bobot']
    )
    komponen.save()
    return redirect('penilaianIndex')

def hapusKomponen(request,idKomponen):
    komponen = KomponenPenilaian.objects.get(id=idKomponen)
    komponen.delete()
    return redirect('penilaianIndex')

def nilaiSiswa(request,idKomponen):
    checkAuthentication(request)
    kelasList = Kelas.objects.values('unique_id').distinct()
    kelasList = sorted(kelasList, key=lambda x: x['unique_id'], reverse=True)
    nilai_prefetch = Prefetch(
        'nilai_set',
        queryset=Nilai.objects.prefetch_related('siswa__user_profile'),
        to_attr='nilai_list'
    )
    
    allSiswa = Siswa.objects.prefetch_related(nilai_prefetch).all()
    return render(request, 'penilaian/nilai_siswa.html', {'allSiswa':allSiswa,'idKomponen':int(idKomponen),'allKelas':kelasList})

def inputNilai(request):
    kp = KomponenPenilaian.objects.get(id=request.POST['idKomponen'])
    siswaList = []
    for key in request.POST:
        if key.startswith('nilai-'):
            if request.POST[key] != '':
                siswaList.append(key.replace('nilai-',''))
    for k in siswaList:
        currSiswa = Siswa.objects.get(id=k)
        currNilai = request.POST['nilai-'+k]
        currSiswa.komponen_penilaian.remove(kp)
        currSiswa.komponen_penilaian.add(kp, through_defaults={'nilai':currNilai})
    return redirect('penilaianIndex')


    
    