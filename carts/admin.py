from django.contrib import admin
from .models import cart, cart_item, categoryoffer, coupon, couponuseduser, productoffer

# Register your models here.
admin.site.register(cart)
admin.site.register(cart_item)
admin.site.register(categoryoffer)
admin.site.register(productoffer)
admin.site.register(coupon)
admin.site.register(couponuseduser)

