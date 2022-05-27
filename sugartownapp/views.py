from asyncio.windows_events import NULL
from datetime import datetime
from os import path
from re import I
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sugartownapp.detection import FaceRecognition
from sugartownapp.detection1 import FaceRecognition1
from django.db.models import Sum
from sugartownapp.models import UserProfile, userfaceid, userrequirements, latestoffers_user, user_contactinfo, newsletter_user, user_cart, discount_coupons, user_cart_value, user_wallet, user_order, userorderdetails
import cv2
from django.core.files import File
from django.contrib.auth.hashers import check_password

# calling face recognition class from detection.py files
faceRecognition = FaceRecognition()
faceRecognition1 = FaceRecognition1()

# functions for calculating total cart cost and total cart in items


def cartitem(request):
    username = get_user(request)
    total_cart_item = user_cart.objects.filter(username=username).aggregate(
        TOTAL=Sum('quantity'))['TOTAL']
    if total_cart_item == None:
        total_cart_item = 0
    return total_cart_item


def cartcost(request):
    username = get_user(request)
    if user_cart_value.objects.filter(username=username).exists():

        total_cart_cost = user_cart_value.objects.get(
            username=username).total_cart_value
    else:
        total_cart_cost = user_cart.objects.filter(username=username).aggregate(
            TOTAL=Sum('total_price'))['TOTAL']

    if total_cart_cost == None:
        total_cart_cost = 0
    return total_cart_cost


def changecost(request):
    username = get_user(request)
    cost_change = user_cart.objects.filter(username=username).aggregate(
        TOTAL=Sum('total_price'))['TOTAL']

    return cost_change


# functions for login, register and home page and logout
def index(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'index.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'index.html')


def loginuser(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            face = userfaceid.objects.get(username=username).id_face
            print("face", face)
            face_id = faceRecognition.recognizeFace(face)
            print("\nfaceid", face_id)

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
                user_wallet_username = user_wallet(username=username)
                user_wallet_username.save()

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


# function to call the detection.py file for face recognition
def addFace(request, username):

    user_username = username
    face_id = userfaceid.objects.get(username=user_username).id_face
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/')


# fucntions for user requirements, offers
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


# functions for about, contact, blog
def about(request):

    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'about.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
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

    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'contact.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:

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

    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'blog.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:

        return render(request, 'blog.html')


# functions for account, shop
@login_required(login_url='/login/')
def account(request):
    if request.user.is_authenticated:
        username = get_user(request)
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        wallet_balance = user_wallet.objects.get(
            username=username).wallet_balance

        if wallet_balance == None:
            wallet_balance = 0

        user_order_history = user_order.objects.filter(username=username).all()

        return render(request, 'account.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost, 'wallet_balance': wallet_balance, 'user_order_history': user_order_history})
    else:
        return render(request, 'account.html')


def shop(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop.html')


#  functions for switching to different products page
def shop_products(request):
    if request.method == "POST":
        type_product_value = request.POST.get('producttype')
        if type_product_value == "Cupcake" or type_product_value == "cupcake" or type_product_value == "cupCake" or type_product_value == "cupCakes" or type_product_value == "CupCakes" or type_product_value == "Cupcakes" or type_product_value == "cupcakes":
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
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop-cake.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop-cake.html')


def shop_products_chocolates(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop-chocolates.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop-chocolates.html')


def shop_products_cookies(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop-cookies.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop-cookies.html')


def shop_products_donuts(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop-donuts.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop-donuts.html')


def shop_products_icecreams(request):
    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'shop-icecreams.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'shop-icecreams.html')


# functions for shop cart functionality
@login_required(login_url='/login/')
def shop_cart(request):
    username = get_user(request)
    user_cart_items = user_cart.objects.filter(username=username).all()

    total_cart_cost = user_cart.objects.filter(username=username).aggregate(
        TOTAL=Sum('total_price'))['TOTAL']

    total_cart_item = cartitem(request)

    couponcode = discount_coupons.objects.all()

    total_cart_cost = cartcost(request)
    if total_cart_cost == None:
        total_cart_cost = 0
    print("value ", total_cart_cost)
    wallet_balance = user_wallet.objects.get(
        username=username).wallet_balance

    if wallet_balance == None:
        wallet_balance = 0

    return render(request, 'shoping-cart.html', {'cart_detail': user_cart_items, 'total_cart_item': total_cart_item, 'discount_coupons': couponcode, 'total_cart_cost': total_cart_cost, 'wallet_balance': wallet_balance})


# functions for adding products to cart
@login_required(login_url='/login/')
def cart_add(request, product_name, product_price):
    username = get_user(request)
    # print(product_name)
    # print(product_price)
    if user_cart.objects.filter(username=username, product_name=product_name).exists():
        cartvalue = user_cart.objects.get(
            username=username, product_name=product_name).quantity

        user_cart.objects.filter(
            username=username, product_name=product_name).update(quantity=cartvalue + 1)

        cartvalue = user_cart.objects.get(
            username=username, product_name=product_name).quantity

        user_cart.objects.filter(
            username=username, product_name=product_name).update(total_price=cartvalue * product_price)

        total_cart_value = changecost(request)

        print(total_cart_value)

        coupon_applied = user_cart_value.objects.get(
            username=username).coupon_applied

        if coupon_applied != "None":
            coupon_discount = discount_coupons.objects.get(
                couponcode=coupon_applied).discount_percent
            coupon_valid_price = discount_coupons.objects.get(
                couponcode=coupon_applied).validprice

            coupon_discount = (100-coupon_discount)/100

            if total_cart_value > coupon_valid_price:
                user_cart_value.objects.filter(username=username).update(
                    total_cart_value=total_cart_value*coupon_discount)
            else:
                user_cart_value.objects.filter(username=username).update(
                    total_cart_value=total_cart_value)
        else:
            user_cart_value.objects.filter(username=username).update(
                total_cart_value=total_cart_value)

        messages.info(
            request, f'{product_name} added successfully to cart!!', product_name)
        return redirect('/shop/')
    else:

        user_cart_product = user_cart(
            username=username, product_name=product_name, product_price=product_price, quantity=1, total_price=product_price)
        user_cart_product.save()
        total_cart_value = changecost(request)
        print(total_cart_value)
        if user_cart_value.objects.filter(username=username).exists():
            total_cart_value = changecost(request)
            print(total_cart_value)
            coupon_applied = user_cart_value.objects.get(
                username=username).coupon_applied
            print(coupon_applied)

            if coupon_applied != "None":
                coupon_discount = discount_coupons.objects.get(
                    couponcode=coupon_applied).discount_percent
                coupon_valid_price = discount_coupons.objects.get(
                    couponcode=coupon_applied).validprice

                coupon_discount = (100-coupon_discount)/100

                if total_cart_value > coupon_valid_price:
                    user_cart_value.objects.filter(username=username).update(
                        total_cart_value=total_cart_value*coupon_discount)
                else:
                    user_cart_value.objects.filter(username=username).update(
                        total_cart_value=total_cart_value)
            else:
                user_cart_value.objects.filter(username=username).update(
                    total_cart_value=total_cart_value)

        else:
            total_value = user_cart_value(
                username=username, total_cart_value=total_cart_value)
            total_value.save()

        messages.info(
            request, f"{product_name} added successfully to cart!!", product_name)
        return redirect('/shop/')


#  functions for deleting items from cart
@login_required(login_url='/login/')
def delete_cart_item(request, product_name):
    username = get_user(request)
    delete_item = user_cart.objects.get(
        username=username, product_name=product_name)
    delete_item.delete()
    total_cart_value = changecost(request)
    print(total_cart_value)
    coupon_applied = user_cart_value.objects.get(
        username=username).coupon_applied

    if coupon_applied != "None":
        coupon_discount = discount_coupons.objects.get(
            couponcode=coupon_applied).discount_percent
        coupon_valid_price = discount_coupons.objects.get(
            couponcode=coupon_applied).validprice

        coupon_discount = (100-coupon_discount)/100

        if total_cart_value > coupon_valid_price:
            user_cart_value.objects.filter(username=username).update(
                total_cart_value=total_cart_value*coupon_discount)
        else:
            user_cart_value.objects.filter(username=username).update(
                total_cart_value=total_cart_value)
    else:
        user_cart_value.objects.filter(username=username).update(
            total_cart_value=total_cart_value)
    messages.success(
        request, f'{product_name} removed successfully from cart!')
    return redirect('/cart')

# functions for altering cart


@login_required(login_url='/login/')
def alter_cart(request, product_name):
    if request.method == "POST":
        username = get_user(request)
        alteredquantity = request.POST.get('quantityproduct')
        print(alteredquantity)

        user_cart.objects.filter(
            username=username, product_name=product_name).update(quantity=alteredquantity)

        cartvalue = user_cart.objects.get(
            username=username, product_name=product_name).quantity

        productprice = user_cart.objects.get(
            username=username, product_name=product_name).product_price

        user_cart.objects.filter(
            username=username, product_name=product_name).update(total_price=cartvalue * productprice)

        total_cart_value = changecost(request)
        print(total_cart_value)
        coupon_applied = user_cart_value.objects.get(
            username=username).coupon_applied

        if coupon_applied != "None":
            coupon_discount = discount_coupons.objects.get(
                couponcode=coupon_applied).discount_percent
            coupon_valid_price = discount_coupons.objects.get(
                couponcode=coupon_applied).validprice

            coupon_discount = (100-coupon_discount)/100

            if total_cart_value > coupon_valid_price:
                user_cart_value.objects.filter(username=username).update(
                    total_cart_value=total_cart_value*coupon_discount)
            else:
                user_cart_value.objects.filter(username=username).update(
                    total_cart_value=total_cart_value)
        else:
            user_cart_value.objects.filter(username=username).update(
                total_cart_value=total_cart_value)
        messages.success(
            request, f'{product_name} updated Successfully!')
        return redirect('/cart')
    return render(request, 'shoping-cart.html')

# functions for discount_coupon functionality


@login_required(login_url='/login/')
def discount_coupon(request):
    if request.method == "POST":
        username = get_user(request)
        couponname = request.POST.get('couponname')

        if discount_coupons.objects.filter(couponcode=couponname).exists():
            coupon_exists = 'False'

            coupon = user_cart_value.objects.get(
                username=username).coupon_applied

            cartcost = user_cart_value.objects.get(
                username=username).total_cart_value

            cost = discount_coupons.objects.get(
                couponcode=couponname).validprice

            if coupon != couponname and cartcost >= cost:
                coupon_discount = discount_coupons.objects.get(
                    couponcode=couponname).discount_percent

                coupon_discount = (100-coupon_discount)/100

                user_cart_value.objects.filter(
                    username=username).update(total_cart_value=cartcost*coupon_discount)

                user_cart_value.objects.filter(
                    username=username).update(coupon_applied=couponname)

                messages.success(request, 'Coupon Applied Successfully!!')
                return redirect('/checkout')
            elif cartcost < cost:
                messages.warning(
                    request, 'Coupon Not Available for the cart amount!!')
                return redirect('/checkout')
            else:
                messages.warning(request, 'Coupon already applied!!')
                return redirect('/checkout')
        else:
            messages.warning(request, 'No Such Coupon exists!!')
            return redirect('/checkout')

    return render(request, 'shoping-cart.html')


# functions for payment checkout functionality
@login_required(login_url='/login/')
def checkout(request):

    cart_item = cartitem(request)

    if cart_item != 0:

        if request.method == "POST":
            username = get_user(request)
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            country = request.POST.get('country')
            street = request.POST.get('street')
            apartment = request.POST.get('apartment')
            city = request.POST.get('town')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            total_payable_amount = user_cart_value.objects.get(
                username=username).total_cart_value
            user_wallet_balance = user_wallet.objects.get(
                username=username).wallet_balance

            if len(phone) == 10 and user_wallet_balance >= total_payable_amount:
                face = userfaceid.objects.get(
                    username=username).id_face
                print("face", face)
                face_id = faceRecognition1.recognizeFace(face)
                print("faceid", face_id)
                if face == face_id:
                    current_time = datetime.now()
                    print(current_time)
                    user_wallet.objects.filter(username=username).update(
                        wallet_balance=user_wallet_balance-total_payable_amount)
                    user_order_data = user_order(username=username, fname=fname, lname=lname, country=country, street=street,
                                                 apartment=apartment, city=city, postcode=postcode, phone=phone, email=email, total_payable_amount=total_payable_amount, total_items=cart_item, orderplaced_on=current_time)

                    user_order_data.save()
                    user_products = user_cart.objects.filter(username=username).values_list(
                        'product_name')

                    user_quantity = user_cart.objects.filter(username=username).values_list(
                        'quantity')

                    for i, j in zip(user_products, user_quantity):
                        user_orderdetails_data = userorderdetails(
                            username=username, product_name=i[0], quantity=j[0])

                        user_orderdetails_data.save()

                    user_cart_delete = user_cart.objects.filter(
                        username=username).all()
                    user_cart_delete.delete()

                    user_cart_value.objects.filter(
                        username=username).update(total_cart_value=0)

                    user_cart_value.objects.filter(
                        username=username).update(coupon_applied="None")

                    messages.success(request, 'Order Placed Successfully')
                    user_wallet_balance_email = user_wallet.objects.get(
                        username=username).wallet_balance
                    user_email = UserProfile.objects.get(
                        username=username).email
                    subject = 'SugarTown Wallet Alert'
                    html_message = render_to_string(
                        'wallet_alert.html', {'deducted_amount': total_payable_amount, 'wallet_balance': user_wallet_balance_email})
                    plain_message = strip_tags(html_message)
                    from_email = 'sugartown20@gmail.com'
                    to = user_email
                    send_mail(subject, plain_message, from_email,
                              [to], html_message=html_message, fail_silently=False)

                    subject = 'no reply (order Confirmation from Sugartown)'
                    html_message = render_to_string(
                        'mail_template.html', {'fname': fname, 'lname': lname, 'total_item': cart_item, 'total_cost': total_payable_amount})
                    plain_message = strip_tags(html_message)
                    from_email = 'sugartown20@gmail.com'
                    to = user_email
                    send_mail(subject, plain_message, from_email,
                              [to], html_message=html_message, fail_silently=False)

                    return redirect('/')
                elif face != face_id:
                    messages.warning(
                        request, 'Sorry! Not able to match the face associated with this account, Order Not Placed')
                    return redirect('/checkout')

            elif len(phone) != 10:
                messages.warning(request, 'Invalid Contact Number!!')
                return redirect('/checkout')

            elif total_payable_amount > user_wallet_balance:
                messages.warning(request, 'Insufficient Wallet Balance!!')
                return redirect('/checkout')

        if request.user.is_authenticated:
            total_cart_item = cartitem(request)
            total_cart_cost = cartcost(request)
            couponcode = discount_coupons.objects.all()
            username = get_user(request)
            product_details = user_cart.objects.filter(username=username).all()

            cart_value = user_cart_value.objects.get(
                username=username).total_cart_value

            user_wallet_balance = user_wallet.objects.get(
                username=username).wallet_balance

            return render(request, 'checkout.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost, 'discount_coupons': couponcode, 'cart_products': product_details, 'total_cart_value': cart_value, 'wallet_balance': user_wallet_balance})
        else:
            return render(request, 'checkout.html')

    else:
        messages.warning(request, "No Items Present in the Cart!!")
        return redirect('/shop/cart')


# function for adding balance to wallet
@login_required(login_url='/login/')
def add_balance(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        amount = request.POST.get('amount')

        user_exists = 'False'
        username_account = get_user(request)
        username_account = str(username_account)

        if user_wallet.objects.filter(username=username).exists():
            user_exists = 'True'

        user_username = 'False'

        if username == username_account:
            user_username = 'True'

        if user_exists == 'True' and user_username == 'True':
            account_password = User.objects.get(username=username).password
            checkpassword = check_password(password, account_password)

            if checkpassword == True:
                face = userfaceid.objects.get(
                    username=username_account).id_face
                print("face", face)
                face_id = faceRecognition1.recognizeFace(face)
                print("faceid", face_id)
                if face == face_id:
                    balance = user_wallet.objects.get(
                        username=username).wallet_balance
                    user_wallet.objects.filter(username=username).update(
                        wallet_balance=balance+int(amount))
                    # face_id = -1
                    messages.success(
                        request, f'{amount} added Successfully to Sugar Town Wallet!!')
                    return redirect('/account')
                elif face != face_id:
                    messages.warning(
                        request, 'Sorry! Not able to match the face associated with this account')
                    return redirect('/account')

            elif checkpassword == False:
                messages.warning(
                    request, 'Sorry! Not able to match the password associated with this account')
                return redirect('/account')

        elif user_exists == 'False' and user_username == 'True':
            account_password = User.objects.get(username=username).password
            checkpassword = check_password(password, account_password)

            if checkpassword == True:
                face = userfaceid.objects.get(
                    username=username_account).id_face
                print("face", face)
                face_id = faceRecognition1.recognizeFace(face)
                print("faceid", face_id)
                if face == face_id:
                    wallet_update = user_wallet(
                        username=username, wallet_balance=amount)
                    wallet_update.save()
                    # face_id = -1
                    messages.success(
                        request, f'{amount} added Successfully to Sugar Town Wallet!!')
                    return redirect('/account')
                elif face != face_id:
                    messages.warning(
                        request, 'Sorry! Not able to match the face associated with this account')
                    return redirect('/account')

            elif checkpassword == False:
                messages.warning(
                    request, 'Sorry! Not able to match the password associated with this account')
                return redirect('/account')

        elif user_username == 'False':
            messages.warning(
                request, 'Sorry! Not able to find the username entered in our Databases')
            return redirect('/account')

    if request.user.is_authenticated:
        total_cart_item = cartitem(request)
        total_cart_cost = cartcost(request)
        return render(request, 'balance.html', {'total_cart_item': total_cart_item, 'total_cart_cost': total_cart_cost})
    else:
        return render(request, 'balance.html')
