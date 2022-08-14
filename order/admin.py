from django.contrib import admin

from order.models import order, order_product, payment

# Register your models here.
admin.site.register(order)
admin.site.register(order_product)
admin.site.register(payment)