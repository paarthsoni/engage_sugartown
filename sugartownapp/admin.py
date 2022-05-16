from django.contrib import admin
from sugartownapp.models import UserProfile, userfaceid, userrequirements, latestoffers_user, user_contactinfo
# # Register your models here.

admin.site.register(UserProfile)
admin.site.register(userfaceid)
admin.site.register(userrequirements)
admin.site.register(latestoffers_user)
admin.site.register(user_contactinfo)
