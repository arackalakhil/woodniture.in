from itertools import product
from multiprocessing import reduction
from optparse import Values
from pickle import TRUE
from re import T
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from products.models import categories, products
from carts.models import  cart, cart_item, categoryoffer, coupon, couponuseduser, productoffer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from users.models import address

# Create your views here.
# def offer_check(item):
#     offer_price_category=0
#     # offer_price_product=0
#     product =products.objects.get(name=item.product.name)
#     print(product)
#     products_offer=productoffer.objects.filter(product=product,active=True)
#     print(products_offer)
#     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#     real_price= product.price
#     if products_offer.exists():
#         if product.product_offer:
#             offer_price_product= product.price-(product.price*product.product_offer.discount/100)
#     else:
#         offer_price_product =product.price
    
#     category_offer =categoryoffer.objects.filter(category=product.cats)
#     category =categories.objects.get(category_name=product.cats)
#     if category_offer.exists():
        # if category_offer.category.cats_offers:
            # offer_price_category = product.price - (product.price*product.cats.cats_offers.discount/100)
    #         print('gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg')
            
    # else:
    #         offer_price_category = product.price 
    # offer_price_category = real_price
    # if category_offer.exists() &  products_offer.exists():
    #     if offer_price_category < offer_price_product:
    #             return offer_price_category
            
    #     else:
    #         return offer_price_product
    # else:
    #     if products_offer.exists():
    #         return offer_price_product
    #     elif category_offer.exists():
    #         return offer_price_category
    #     else:
    #         return real_price
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
global discount
discount = 0

# def offer_check(item):
#     product =products.objects.get(name=item.product.name)
#     print(product)
#     products_offer=productoffer.objects.filter(product=product,is_active=True)
#     print(products_offer)
#     real_price= product.price
#     if products_offer.exists():
#         if product.product_offer:
#             offer_price_product= product.price-(product.price* product.product_offer.discount/100)
#             product.product_new_price=offer_price_product
#             product.save()
#     else:
#         offer_price_product = product.price
#         product.product_new_price=offer_price_product
#         product.save()
    
#     categoriess =categories.objects.get(category_name=item.product.cats)  
#     if categoriess.offer:
#             offer_price_categories= product.price-(product.price*categoriess.offer/100)
#             categoriess.category_new_price=offer_price_categories
#             categoriess.save()
#     else:
#         offer_price_categories = product.price
#         categoriess.category_new_price=offer_price_categories
#         categoriess.save()

    
#     if offer_price_categories >offer_price_product :
#         categoriess.category_new_price=offer_price_product
#         categoriess.save()

#         return offer_price_product
#     elif offer_price_product > offer_price_categories:
#         product.product_new_price=offer_price_categories
#         product.save()
#     else:
#         categoriess.category_new_price=product.price
#         categoriess.save()
#         product.product_new_price=product.price
#         product.save()


#     return offer_price_categories

# def offer_check(item):
#     product =products.objects.get(name=item.product.name)
#     print(product)
#     products_offer=productoffer.objects.filter(product=product,is_active=True)
#     if products_offer.exists():
#         if product.product_offer:
#             offer_price_product= product.price-(product.price* product.product_offer.discount/100)
           
#     else:
#         offer_price_product = product.price
#         product.product_new_price=offer_price_product
#     return offer_price_product


def offer_check(item):
    product =products.objects.get(name=item.product.name)
    print(product)
    offer_price_product=0
    offer_price_category=0
    if productoffer.objects.filter(product=product,is_active=True).exists():
        if product.product_offer:
            offer_price_product= product.price-(product.price* product.product_offer.discount/100)
           
    else:
        offer_price_product = product.price
      
    
    if categoryoffer.objects.filter(category=item.product.cats).exists():
        if item.product.cats.cats_offers:
                offer_price_category = product.price - product.price*product.cats.cats_offers.discount/100
    else:
        offer_price_category = product.price
           

    if offer_price_category <= offer_price_product:
        return offer_price_category
    else:
        return offer_price_product



def cart_id(request):
    session_id = request.session.session_key  # to get session_id(key)/cart id

    if not session_id:  # if session id is not present
        session_id = request.session.create()  # to create a new session
    return session_id


def cat_add(request, id):
    product = products.objects.get(id=id)

    # --------------------- to combain the product and cart-----------------
    if request.user.is_authenticated:       
        try:
            carts_item = cart_item.objects.get(product=product, user=request.user)
            carts_item.quantity += 1  # present cart_item quantibty + 1
            carts_item.save()
        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, user=request.user, quantity=1
            )  # quantity is one since we are creating new cart
            carts_item.save()

    else:
        try:
            carts = cart.objects.get(
            cart_id=cart_id(request)
            )  # to bring cart id from the session
        except cart.DoesNotExist:
            carts = cart.objects.create(cart_id=cart_id(request))
            carts.save()
        try:
            carts_item = cart_item.objects.get(product=product, cart=carts)
            carts_item.quantity += 1
            carts_item.save()

        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, cart=carts, quantity=1
            )
            carts_item.save()
    # return render(request,'cart_list.html')
    
    return redirect(cart_view)

def cart_view(request, total=0, quantity=0, carts_item=0,new_total=0):
    # product =products.objects.all()
    if "coupon_code" in request.session:
        coupons = coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0
    try:

        if request.user.is_authenticated:
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
        
     

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_item = cart_item.objects.filter(cart=carts, is_active=True)
            
            
        for item in carts_item:
            # new_price=offer_price()
            new=offer_check(item)
            print(new) 
            total += new * item.quantity
            print(total)
            quantity += item.quantity
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
    except ObjectDoesNotExist:
        pass
    
    values = {"total": total, "quantity": quantity, "carts_item": carts_item,"new_total":new_total,"reduction":reduction}
    return render(request, "cart_list.html", values)


def delete_cart(request, id):
    total=0 
    quantity=0
    carts_item=None
    new_total=0
    product = get_object_or_404(products, id=id)
    if request.user.is_authenticated:
        carts_item = cart_item.objects.get(product=product, user=request.user)
    else:
        carts = cart.objects.get(cart_id=cart_id(request))
        carts_item = cart_item.objects.get(product=product, cart=carts)
    carts_item.delete()
    if "coupon_code" in request.session:
        coupons = coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0
    try:

        if request.user.is_authenticated:
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
        
     

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_item = cart_item.objects.filter(cart=carts, is_active=True)
            
            
        for item in carts_item:
            # new_price=offer_price()
            new=offer_check(item)
            print(new) 
            total += new * item.quantity
            print(total)
            quantity += item.quantity
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
    except ObjectDoesNotExist:
        pass
    
    values = {"total": total, "quantity": quantity, "carts_item": carts_item,"new_total":new_total,"reduction":reduction}
    return render(request, "htmx_cart.html", values)


def adds_cart(request, id):
    product = products.objects.get(id=id)
    total=0 
    quantity=0
    carts_item=None
    new_total=0

    # --------------------- to combain the product and cart-----------------
    if request.user.is_authenticated:       
        try:
            carts_item = cart_item.objects.get(product=product, user=request.user)
            carts_item.quantity += 1  # present cart_item quantibty + 1
            carts_item.save()
        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, user=request.user, quantity=1
            )  # quantity is one since we are creating new cart
            carts_item.save()

    else:
        try:
            carts = cart.objects.get(
            cart_id=cart_id(request)
            )  # to bring cart id from the session
        except cart.DoesNotExist:
            carts = cart.objects.create(cart_id=cart_id(request))
            carts.save()

        try:
            carts_item = cart_item.objects.get(product=product, cart=carts)
            carts_item.quantity += 1
            carts_item.save()

        except cart_item.DoesNotExist:
            carts_item = cart_item.objects.create(
                product=product, cart=carts, quantity=1
            )
            carts_item.save()
    if "coupon_code" in request.session:
        coupons = coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0
    try:

        if request.user.is_authenticated:
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
        
     

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_item = cart_item.objects.filter(cart=carts, is_active=True)
            
            
        for item in carts_item:
            # new_price=offer_price()
            new=offer_check(item)
            print(new) 
            total += new * item.quantity
            print(total)
            quantity += item.quantity
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
    except ObjectDoesNotExist:
        pass
    
    values = {"total": total, "quantity": quantity, "carts_item": carts_item,"new_total":new_total,"reduction":reduction}
    return render(request, "htmx_cart.html", values)

def cart_item_remove(request, id):
    total=0 
    quantity=0
    carts_item=None
    new_total=0
    product = get_object_or_404(products, id=id)

    if request.user.is_authenticated:
        carts_item = cart_item.objects.get(product=product, user=request.user)

    else:
        carts = cart.objects.get(cart_id=cart_id(request))
        carts_item = cart_item.objects.get(product=product, cart=carts)
    if carts_item.quantity > 1:
        carts_item.quantity -= 1
        carts_item.save()

    else:
        carts_item.delete()
    if "coupon_code" in request.session:
        coupons = coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction = coupons.discount_percentage
    else:
        reduction = 0
    try:

        if request.user.is_authenticated:
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
        
     

        else:
            carts = cart.objects.get(cart_id=cart_id(request))
            carts_item = cart_item.objects.filter(cart=carts, is_active=True)
            
            
        for item in carts_item:
            # new_price=offer_price()
            new=offer_check(item)
            print(new) 
            total += new * item.quantity
            print(total)
            quantity += item.quantity
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
    except ObjectDoesNotExist:
        pass
    
    values = {"total": total, "quantity": quantity, "carts_item": carts_item,"new_total":new_total,"reduction":reduction}
    return render(request, "htmx_cart.html", values)
    return redirect(cart_view)


def checkout(
    request,
    total=0,
    quantity=0,
    new_total=0,    
    cars_items=None, 
):
    if request.user.is_authenticated:
        carts_item = cart_item.objects.filter(user=request.user, is_active=True)
        if not carts_item:
            return redirect('mycart')
      

    else:
        return redirect('mycart')

    if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
    else:
        reduction = 0
    try:
        if request.user.is_authenticated:
            details = address.objects.filter(user=request.user)
            carts_item = cart_item.objects.filter(user=request.user, is_active=True)

        else:
            return render(request,"login-register")
        for item in carts_item:
            print(offer_check(item))
            total += offer_check(item)* item.quantity
            quantity += item.quantity
        if reduction > 0:
                new_total= total-reduction*total/100
        else:
            new_total=total
    except:
        if request.user.is_authenticated:
            pass
        else:
            return render(request,"login-register.html")
    values = {
            "total": total,
            "quantity": quantity,
            "carts_item": carts_item,
            "details": details,
            "new_total":new_total,
            "reduction":reduction,
        }

    return render(request, "checkout.html",values)

def apply_coupon(request):
    if request.method == "POST":
        coupon_code =request.POST.get("coupon_code")
        print(coupon_code)
        try:
            if coupon.objects.get(coupon_code=coupon_code):
                coupon_exist= coupon.objects.get(coupon_code=coupon_code)

                print(coupon_exist)
                try:            
                    if couponuseduser.objects.get(user=request.user,coupon=coupon_exist):
                        messages.error(request, "coupon already applied")
                        return redirect(cart_view)
                except:
                    request.session["coupon_code"]=coupon_code
            else:
                messages.error(request, "coupon already don't exists")
                return redirect(cart_view)
                
        except:
            messages.error(request, "coupon  don't exists")

    return redirect(cart_view)
