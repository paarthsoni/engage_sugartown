from importlib.resources import read_text
from os import path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from requests import ReadTimeout, get
from sympy import re


from sugartownapp.detection import FaceRecognition


from sugartownapp.models import UserProfile, userfaceid, userrequirements, latestoffers_user, user_contactinfo, newsletter_user
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
            print(face)
            face_id = faceRecognition.recognizeFace()
            print(face_id)
            if face_id == face:
                login(request, user)
                messages.success(
                    request, "Logged in successfully as "+username)
                return redirect('/')
            else:

                messages.warning(
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


def userrequirements_data(request):
    if request.method == "POST":
        username = get_user(request)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        requirements = request.POST.get('requirements')

        if len(phone) == 10 and len(requirements) <= 2500:

            user_requirements_data = userrequirements(
                name=name, username=username,  contact=phone, email=email, requirements=requirements)
            user_requirements_data.save()
            messages.success(
                request, "Your Requirements are submitted Successfully! Our Person Will contact you soon")
            return redirect('/')
        elif len(phone) != 10:
            messages.warning(
                request, "Invalid Contact Number")
            return redirect('/')
        elif len(requirements) > 2500:
            messages.warning(
                request, "Requirements Content Limit Exceeded!")
            return redirect('/')

    return render(request, 'index.html')


def latestoffers_user_email_data(request):
    if request.method == "POST":
        username = get_user(request)
        email = request.POST.get('emailid')
        email_exists = False

        if latestoffers_user.objects.filter(email=email).exists():
            email_exists = True

        if email_exists == False:
            userinfo = latestoffers_user(username=username, email=email)
            userinfo.save()
            messages.success(
                request, "Email Registered For latest offers and updates Successfully!")
            return redirect('/')
        elif email_exists == True:
            messages.warning(
                request, "Sorry!! This Email is already registered with us for latest updates and offers")
            return redirect('/')

    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        username = get_user(request)
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if len(message) <= 2500:
            user_contact_data = user_contactinfo(
                username=username, name=name, email=email, message=message)
            user_contact_data.save()
            messages.success(
                request, "Your Message Submitted Successfully!! Our Representative will Contact you soon")

            return redirect('/contact/')
        elif len(message) > 2500:
            messages.warning(
                request, " Sorry Message Length Exceeded!!")

            return redirect('/contact/')

    return render(request, 'contact.html')


def blog(request):
    if request.method == "POST":
        username = get_user(request)
        email = request.POST.get('email')
        email_exists = False

        if newsletter_user.objects.filter(email=email).exists():
            email_exists = True

        if email_exists == False:
            userinfo = newsletter_user(username=username, email=email)
            userinfo.save()
            messages.success(
                request, "Email Registered For Sugar Town Newsletter Successfully!")
            return redirect('/blog')
        elif email_exists == True:
            messages.warning(
                request, "Sorry!! This Email is already registered with us for Sugar Town Newletters")
            return redirect('/blog/')
    return render(request, 'blog.html')


def account(request):
    return render(request, 'account.html')


def shop(request):
    return render(request, 'shop.html')


def shop_products(request):
    if request.method == "POST":
        type_product_value = request.POST.get('producttype')
        if type_product_value == "Cupcake" or type_product_value == "cupcake" or type_product_value == "cupCake":
            return redirect('/shop/')
        elif type_product_value == "Cake" or type_product_value == "Cakes" or type_product_value == "cake" or type_product_value == "cakes":
            return redirect('/shop/products/Cakes')
        elif type_product_value == "Chocolate" or type_product_value == "Chocolates" or type_product_value == "chocolate" or type_product_value == "chocolates":
            return redirect('/shop/products/Chocolates')
        elif type_product_value == "Cookies" or type_product_value == "Cookie" or type_product_value == "cookie" or type_product_value == "cookies":
            return redirect('/shop/products/Cookies')
        elif type_product_value == "Donut" or type_product_value == "Donuts" or type_product_value == "donut" or type_product_value == "donuts":
            return redirect('/shop/products/Donuts')
        elif type_product_value == "icecream" or type_product_value == "icecreams" or type_product_value == "Icecreams" or type_product_value == "Icecream" or type_product_value == "IceCream" or type_product_value == "IceCreams" or type_product_value == "Ice-Cream" or type_product_value == "Ice-Creams" or type_product_value == "ice-cream" or type_product_value == "ice-creams":
            return redirect('/shop/products/icecreams')
        else:
            messages.warning(request, "Sorry!! Product Not Found")
            return redirect('/shop/')
    return render(request, 'shop.html')


def shop_products_cakes(request):
    return render(request, 'shop-cake.html')


def shop_products_chocolates(request):
    return render(request, 'shop-chocolates.html')


def shop_products_cookies(request):
    return render(request, 'shop-cookies.html')


def shop_products_donuts(request):
    return render(request, 'shop-donuts.html')


def shop_products_icecreams(request):
    return render(request, 'shop-icecreams.html')
