from django.contrib import admin
from sugartownapp.models import UserProfile, userfaceid, userrequirements, latestoffers_user, user_contactinfo, newsletter_user, user_cart, discount_coupons, user_cart_value, user_wallet, user_order, userorderdetails
# # Register your models here.

admin.site.register(UserProfile)
admin.site.register(userfaceid)
admin.site.register(userrequirements)
admin.site.register(latestoffers_user)
admin.site.register(user_contactinfo)
admin.site.register(newsletter_user)
admin.site.register(user_cart)
admin.site.register(discount_coupons)
admin.site.register(user_cart_value)
admin.site.register(user_wallet)
admin.site.register(user_order)
admin.site.register(userorderdetails)
