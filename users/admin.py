from django.contrib import admin
from .models import address, customuser, userprofile, wallet

# Register your models here.
admin.site.register(customuser)
admin.site.register(address)
admin.site.register(wallet)

admin.site.register(userprofile)
