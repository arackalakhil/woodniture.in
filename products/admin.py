
from django.contrib import admin

from products.models import banner, categories, products

# Register your models here.
admin.site.register(products)
admin.site.register(categories)
admin.site.register(banner)