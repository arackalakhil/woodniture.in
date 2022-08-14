from audioop import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import re
from carts.models import cart, cart_item, productoffer
from django.core.exceptions import ObjectDoesNotExist
from carts.views import cart_id
from order.models import order_product
from products.models import banner, categories, products
from users.models import wallet

# Create your views here.

def index_page(request):

    banners =banner.objects.filter(is_selected=True).order_by("-id")
    print(banners)
    return render(request,'index.html',{"banners":banners})

def bed_list(request):
    
    category =categories.objects.get(category_name='BED')

    values = products.objects.filter(cats=category).order_by("-id")
    print(values)
  
    return render(request,'userside_productlist.html',{'values':values})

def table_list(request):
    
    category =categories.objects.get(category_name= 'TABLE')

    values = products.objects.filter(cats=category).order_by("-id")
 
  
    return render(request,'userside_productlist.html',{'values':values})


def single_product(request,id):
    values = products.objects.get(id = id )
    return render (request,'single_Product.html',{"values" : values})

# def latest_bed(request):
#     cat=categories.objects.get(category_name="BED")
#     values = products.objects.filter(cats=cat).order_by("-id")[0:1]
#     return render (request,'single_Product.html',{"values" : values})
# def latest_table(request):
#     cat=categories.objects.get(category_name="TABLE")
#     values = products.objects.filter(cats=cat).order_by("-id")[0:1]
#     return render (request,'single_Product.html',{"values" : values})

    
def search(request):
    values = None
    searchvalue =None
    if request.method == 'POST':
        searchvalue = request.POST.get('search')
        print(searchvalue)
        try:
            values = products.objects.get(name__icontains= searchvalue)
            return render(request,'single_Product.html',{"values":values})
        except:
            return render(request,'item_not_found.html')
            

    # return render(request,'single_Product.html',{"values":values})