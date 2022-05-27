from datetime import datetime, timezone
import email
from email import message
from email.policy import default
import uuid
from django.db import models
from numpy import True_
from pkg_resources import Requirement
from sqlalchemy import false
from django.db.models.signals import post_save
from django.contrib.auth.models import User

#  user profile model


class UserProfile(models.Model):
    username = models.CharField(max_length=1024, null=False,
                                unique=False, primary_key=True, default="")
    name = models.CharField(max_length=1024, null=False,
                            unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=True, default="")
    contact = models.CharField(
        max_length=12, null=False, unique=True, default="")
    head_shot = models.ImageField(
        upload_to='user_face_images/', blank=True, default="")

    def __str__(self):
        return self.username


#  model to store user face id
class userfaceid(models.Model):
    id_face = models.AutoField(primary_key=True, default=0)
    username = models.CharField(
        max_length=1024, null=False, unique=True, default="")

    def __str__(self):
        return str(self.id_face)

# model to store requirements for user


class userrequirements(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    name = models.CharField(max_length=1024, null=False,
                            unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=False, default="")
    contact = models.CharField(
        max_length=12, null=False, unique=False, default="")
    requirements = models.CharField(
        max_length=2500, null=False, unique=False, default="")

    def __str__(self):
        return self.name + " - "+self.username


# model to store all the users who are subscribed for latest offers
class latestoffers_user(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=False, default="")

    def __str__(self):
        return self.username + " - "+self.email

# models to store the user input from the contact form


class user_contactinfo(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    name = models.CharField(max_length=1024, null=False,
                            unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=False, default="")
    message = models.CharField(
        max_length=2500, null=False, unique=False, default="")

    def __str__(self):
        return self.name + " - "+self.email


#  model to store users subscribed to news letter
class newsletter_user(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=False, default="")

    def __str__(self):
        return self.username + " - "+self.email


#  model to store the user cart details
class user_cart(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    product_name = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    product_price = models.IntegerField(null=False, unique=False, default=0)
    quantity = models.IntegerField(null=False, unique=False, default=0)
    total_price = models.IntegerField(null=False, unique=False, default=0)
    total_cart_value = models.IntegerField(null=False, unique=False, default=0)

    def __str__(self):
        return self.username

#  model to store the discount_coupons


class discount_coupons(models.Model):
    coupon_name = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    couponcode = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    validprice = models.IntegerField(null=False, unique=False, default=0)
    discount_percent = models.IntegerField(null=False, unique=False, default=0)

    def __str__(self):
        return self.coupon_name

#  model to store the cart value of user


class user_cart_value(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    total_cart_value = models.IntegerField(null=True, unique=False, default=0)
    coupon_applied = models.CharField(
        max_length=1024, null=True, unique=False, default="None")

    def __str__(self):
        return self.username


#  model to store user wallet balance
class user_wallet(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    wallet_balance = models.IntegerField(null=True, unique=False, default=0)

    def __str__(self):
        return self.username


# model to store the user order details

class user_order(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    fname = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    lname = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    country = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    street = models.CharField(
        max_length=1024, null=False, unique=False, default="")

    apartment = models.CharField(
        max_length=1024, null=False, unique=False, default="")

    city = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    postcode = models.CharField(
        max_length=1024, null=False, unique=False, default="")
    phone = models.CharField(
        max_length=12, null=False, unique=False, default="")
    email = models.EmailField(
        max_length=1024, null=False, unique=False, default="")

    total_payable_amount = models.IntegerField(
        null=False, unique=False, default=0)

    total_items = models.IntegerField(
        null=False, unique=False, default=0)

    orderplaced_on = models.DateTimeField(
        auto_now_add=False, blank=False, null=False)

    def __str__(self):
        return self.username+" - "+self.fname+" "+self.lname


#  model to store user order details products
class userorderdetails(models.Model):
    username = models.CharField(
        max_length=1024, null=False, unique=False, default="")

    product_name = models.CharField(
        max_length=1024, null=False, unique=False, default="")

    quantity = models.CharField(
        max_length=1024, null=False, unique=False, default="")

    def __str__(self):
        return self.username
