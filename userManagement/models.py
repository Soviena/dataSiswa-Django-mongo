from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    class Gender(models.TextChoices):
        LAKI_LAKI = 'L', 'Laki-Laki'
        PEREMPUAN = 'P', 'Perempuan'
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama_Lengkap = models.CharField(max_length=255, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=Gender.choices, blank=True, null=True)
    no_hp = models.CharField(max_length=16, blank=True, null=True)
    tempat_lahir = models.CharField(max_length=255, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20)
    pic = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

class feedback(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user_profile.nama_Lengkap}'s feedback"


class Kelas(models.Model):
    unique_id = models.CharField(max_length=10, unique=True, default='None')
    grup = models.CharField(max_length=50)
    tingkat = models.IntegerField()

    def __str__(self):
        return f"{self.tingkat}{self.grup}"

class Pelajaran(models.Model):
    nama = models.CharField(max_length=100)
    singkatan = models.CharField(max_length=20)

    def __str__(self):
        return self.nama

class Guru(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    nip = models.CharField(max_length=20)
    bidang_studi = models.CharField(max_length=50)

    def __str__(self):
        return f"Guru: {self.user_profile.user.username} - NIP: {self.nip}"

class Absensi(models.Model):
    materi = models.CharField(max_length=255)
    catatan = models.TextField()
    tanggal = models.DateField()
    pertemuan = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    pic = models.TextField(blank=True, null=True)
    id_pelajaran = models.ForeignKey(Pelajaran, on_delete=models.CASCADE)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Absensi - Materi: {self.materi}, Tanggal: {self.tanggal}"

class Siswa(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    komponen_penilaian = models.ManyToManyField('KomponenPenilaian', through='Nilai', null=True)
    nis = models.CharField(max_length=20)
    nisn = models.CharField(max_length=20)
    angkatan = models.IntegerField()
    absensi = models.ManyToManyField(Absensi, through='AbsensiSiswa', blank=True, null=True)

    def __str__(self):
        return f"Siswa: {self.user_profile.user.username} - NIS: {self.nis}"

class AbsensiSiswa(models.Model):
    id_absensi = models.ForeignKey(Absensi, on_delete=models.CASCADE)
    id_siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    keterangan = models.CharField(max_length=100)

    def __str__(self):
        return f"AbsensiSiswa - Absensi: {self.id_absensi}, Siswa: {self.id_siswa}"

class KomponenPenilaian(models.Model):
    pelajaran = models.ForeignKey(Pelajaran, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    tahun = models.IntegerField()
    bobot = models.DecimalField(max_digits=5, decimal_places=2)  

class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    komponen_penilaian = models.ForeignKey(KomponenPenilaian, on_delete=models.CASCADE)
    nilai = models.DecimalField(max_digits=5, decimal_places=2)
