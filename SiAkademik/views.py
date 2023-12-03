from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.files.storage import default_storage


from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash


from userManagement.models import UserProfile
# from bson.objectid import ObjectId

import os
import hashlib
# import pymongo
from django.conf import settings

# my_client = pymongo.MongoClient(settings.DB_NAME)

# dbname = my_client['datasiswa'] # Nama Database
# db_users = dbname["users"] # Nama Tabel
# db_login = dbname['login']

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

def auth(request):
    # data = {
    #     "username":request.POST['username']
    # }
    # result = db_login.find_one(data)
    # if result is None:
    #     return redirect('login')
    # if not check_password(request.POST['password'],result['password']):
    #     return redirect('login')
    # request.session['login'] = True
    # request.session['username'] = request.POST['username']
    # request.session['role'] = result['role']
    # request.session['uid'] = str(result['_id'])
    # request.session['uids'] = str(result['_idUser'])
    # request.session['pic'] = "profilePic/"+str(result.get('profilePic'))

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        request.session['username'] = username
        try:
            user_profile = UserProfile.objects.get(user=user)
            request.session['role'] = user_profile.role
            request.session['pic'] = "profilePic/"+str(user_profile.pic)
        except:
            user_profile = UserProfile(user=user, role='ADMIN', pic='default.jpeg')
            user_profile.save()
            request.session['role'] = 'ADMIN'
            request.session['pic'] = 'profilePic/default.jpeg'

        return redirect('home')  # Change 'home' to the desired redirect path
    else:
        error_message = "Invalid username or password"
        # return render(request, 'login.html', {'error_message': error_message})
        return redirect('login')

def logout_fun(request):
    logout(request)
    return redirect('login')

def profile(request,username):
    user_login = request.user
    user_details = UserProfile.objects.get(user=user_login)
    user_details.profilePic = "profilePic/"+str(user_details.pic)

    return render(request, 'profile.html', {'userDetails':user_details,'userLogin':user_login})

def profileEdit(request):
    user_login = request.user
    user_details = UserProfile.objects.get(user=user_login)
    user_details.profilePic = "profilePic/"+str(user_details.pic)
    return render(request, 'profileEdit.html', {'userDetails':user_details,'userLogin':user_login})

def profileUpdate(request):
    # loginData = db_login.find_one({"_id": ObjectId(request.session['uid'])})
    # user_id = loginData['_idUser']
    # userData = db_users.find_one({"_id" : ObjectId(user_id)})
    # data = {
    #     "nama_Lengkap" : request.POST['name'],
    #     "jenis_kelamin" : request.POST['kelamin'],
    #     "tempat_lahir" : request.POST['tempat-lahir'],
    #     "tanggal_lahir" : request.POST['tanggal-lahir'],
    #     "alamat": request.POST['alamat'],
    #     "no_hp": request.POST['phone']
    # }
    # db_users.replace_one({"_id": ObjectId(userData['_id'])},data)

    user_profile = UserProfile.objects.get(user=request.user)

    # Update the UserProfile fields with the provided data
    jk = 'L' if request.POST['kelamin'] == 'Laki-Laki' else 'P'
    user_profile.nama_Lengkap = request.POST['name']
    user_profile.jenis_kelamin = jk
    user_profile.tempat_lahir = request.POST['tempat-lahir']
    user_profile.tanggal_lahir = request.POST['tanggal-lahir']
    user_profile.alamat = request.POST['alamat']
    user_profile.no_hp = request.POST['phone']

    if request.FILES.get('profile-pic'):
        uploaded_file = request.FILES['profile-pic']
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        hashed_file_name = hashlib.sha256(file_name.encode()).hexdigest() + file_extension
        uploaded_file.name = hashed_file_name
        default_storage.save("static/profilePic/"+uploaded_file.name, uploaded_file)
        user_profile.pic = uploaded_file.name
        request.session['pic'] = "profilePic/"+str(uploaded_file.name)
    if request.user.username != request.POST['username']:
        request.user.username = new_username
        request.user.save()
    # db_login.update_one({"_idUser":ObjectId(user_id)},{'$set':{'username':request.POST['username']}})
    if request.POST['password'] != "":
        request.user.set_password(request.POST['password'])
        request.user.save()
        update_session_auth_hash(request, user)
    user_profile.save()
    return redirect('profile',request.POST['username'])