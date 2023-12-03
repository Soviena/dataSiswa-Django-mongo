from django.contrib import admin

# Register your models here.
from .models import UserProfile, Kelas, Pelajaran, Guru, Absensi, Siswa, AbsensiSiswa

admin.site.register(UserProfile)
admin.site.register(Kelas)
admin.site.register(Guru)
admin.site.register(Absensi)
admin.site.register(Siswa)
admin.site.register(AbsensiSiswa)
