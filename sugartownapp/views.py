from os import path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required

from sugartownapp.detection import FaceRecognition


from sugartownapp.models import UserProfile, userfaceid
import cv2
from django.core.files import File

faceRecognition = FaceRecognition()


def index(request):
    return render(request, 'index.html')


def loginuser(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            face = userfaceid.objects.get(username=username).id_face
            face_id = faceRecognition.recognizeFace(face)
            # print(face_id)
            if face_id != -1:
                login(request, user)
                messages.success(
                    request, "Logged in successfully as "+username)
                return redirect('/')
            else:
                messages.success(
                    request, "Sorry Not able to recognize the Face asscociated with this account!!")
                return redirect('/login/')

        else:
            messages.warning(request, 'invalid username or password')
            return redirect("/login")
    messages.warning(
        request, 'Face Image Will be Captured after filling the details, Please Sit in a Proper Position')
    return render(request, 'login.html')


accusername = None


def registeruser(request):
    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        username_exists = False
        email_exists = False
        contact_exists = False
        if User.objects.filter(username=username).exists():
            username_exists = True

        if UserProfile.objects.filter(email=email).exists():
            email_exists = True

        if UserProfile.objects.filter(contact=contact).exists():
            contact_exists = True

        if username_exists == False and email_exists == False and contact_exists == False:
            if(len(username) <= 25 and password == cpassword and len(contact) == 10):
                user = User.objects.create_user(
                    first_name=name, username=username, password=password)
                userdata = UserProfile(
                    username=username, name=name, email=email, contact=contact)
                face_id = userfaceid.objects.latest('id_face').id_face
                face_id = face_id+1
                userfacedata = userfaceid(
                    id_face=face_id, username=username)
                user.save()
                userdata.save()
                userfacedata.save()

                addFace(request, username)
                messages.success(
                    request, 'Your account is created successfully with username: '+username)

                return redirect("/login")
            elif len(username) > 25:
                messages.warning(
                    request, 'Username Length Should be less than 25!')
                return redirect("/login")
            elif password != cpassword:
                messages.warning(
                    request, 'Entered Password do not match')
                return redirect('/login')
            elif len(contact) != 10:
                messages.warning(
                    request, 'Length of contact number should be 10')
                return redirect('/login')
        elif username_exists == True:
            messages.warning(request, "Username already exists!!")
        elif contact_exists == True:
            messages.warning(request, "Contact Number already exists!!")
        elif email_exists == True:
            messages.warning(request, "Email ID already exists!!")
    messages.warning(
        request, 'Face Image Will be Captured after filling the details, Please Sit in a Proper Position')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out Successfully ')
    return redirect("/")


def addFace(request, username):

    user_username = username
    face_id = userfaceid.objects.get(username=user_username).id_face
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/')
