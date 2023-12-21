# Generated by Django 4.2.1 on 2023-12-15 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materi', models.CharField(max_length=255)),
                ('catatan', models.TextField()),
                ('tanggal', models.DateField()),
                ('pertemuan', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('pic', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AbsensiSiswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keterangan', models.CharField(max_length=100)),
                ('id_absensi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.absensi')),
            ],
        ),
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(default='None', max_length=10, unique=True)),
                ('grup', models.CharField(max_length=50)),
                ('tingkat', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KomponenPenilaian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('tahun', models.IntegerField()),
                ('bobot', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Nilai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai', models.DecimalField(decimal_places=2, max_digits=5)),
                ('komponen_penilaian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.komponenpenilaian')),
            ],
        ),
        migrations.CreateModel(
            name='Pelajaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('singkatan', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_Lengkap', models.CharField(blank=True, max_length=255, null=True)),
                ('jenis_kelamin', models.CharField(blank=True, choices=[('L', 'Laki-Laki'), ('P', 'Perempuan')], max_length=1, null=True)),
                ('no_hp', models.CharField(blank=True, max_length=16, null=True)),
                ('tempat_lahir', models.CharField(blank=True, max_length=255, null=True)),
                ('tanggal_lahir', models.DateField(blank=True, null=True)),
                ('alamat', models.TextField(blank=True, null=True)),
                ('role', models.CharField(max_length=20)),
                ('pic', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nis', models.CharField(max_length=20)),
                ('nisn', models.CharField(max_length=20)),
                ('angkatan', models.IntegerField()),
                ('absensi', models.ManyToManyField(blank=True, null=True, through='userManagement.AbsensiSiswa', to='userManagement.absensi')),
                ('id_kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.kelas')),
                ('komponen_penilaian', models.ManyToManyField(null=True, through='userManagement.Nilai', to='userManagement.komponenpenilaian')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userManagement.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='nilai',
            name='siswa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.siswa'),
        ),
        migrations.AddField(
            model_name='komponenpenilaian',
            name='pelajaran',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.pelajaran'),
        ),
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nip', models.CharField(max_length=20)),
                ('bidang_studi', models.CharField(max_length=50)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userManagement.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userManagement.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='absensisiswa',
            name='id_siswa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.siswa'),
        ),
        migrations.AddField(
            model_name='absensi',
            name='id_kelas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.kelas'),
        ),
        migrations.AddField(
            model_name='absensi',
            name='id_pelajaran',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.pelajaran'),
        ),
        migrations.AddField(
            model_name='absensi',
            name='id_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
