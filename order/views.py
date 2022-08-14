from ast import Global
from email import message
import http
import json
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from carts.models import cart, cart_item, coupon, couponuseduser, productoffer
from carts.views import cart_id, cart_view, offer_check
from order.models import order, order_product, payment
from products.models import products
from products.views import index_page
from users.models import address, wallet
from datetime import date
import datetime
from users.views import user_profile
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def invoice(request, carts_item=0):
   new_total=0
   
   if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
   else:
        reduction = 0
   if request.user.is_authenticated:
      if request.method  == "POST":
         global address_id
         address_id=request.POST.get("address_id")
         if address_id is None:
            
            return redirect("checkout")
         global addresss
         addresss=address.objects.get(id = address_id)
         carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
         if not carts_item:
            return redirect ("index_page")

      total=0
      quantity=0
      
      for item in carts_item:
         total += offer_check(item) * item.quantity
         quantity += item.quantity
      if reduction > 0:
            new_total= total-reduction*total/100
      else:
            new_total=total
   else:
      return redirect ("index_page")
   wallet_amount=wallet(user=request.user)
   if wallet_amount.balance > 10:
        amount=total-wallet_amount




   client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
   global payments
   payments =client.order.create({"amount":int(new_total)*100, "currency" : "INR", "payment_capture":1})
   payment_id = payments["id"]
   offer = productoffer.objects.all()
   values ={"addresss":addresss,"carts_item":carts_item,"total":total,"quantity":quantity,"payments":payments,"payment_id":payment_id,"reduction":reduction,"new_total":new_total}
   
   return render (request,"invoice.html",values)



@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def cod(request):
   if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
   else:
        reduction = 0
   user = request.user
   cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
   cart_itemcount = cart_items.count()
   if cart_itemcount <= 0 :
        return redirect ("index_page")

   if request.user.is_authenticated:
      carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
      total=0
      quantity=0
      
      for item in carts_item:
         total += offer_check(item) * item.quantity
         quantity += item.quantity
      if reduction > 0:
            new_total= total-reduction*total/100
      else:
            new_total=total
      cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
      cart_itemcount = cart_items.count()
      if cart_itemcount <= 0 :
         return redirect ("index_page")
      order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
      dates =date.today()
      
      
      payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
      amount = new_total
      payment_method="cashondelivery"
      
      payments = payment(user=user,payment_id=payment_id,amount=amount,date=dates)
      payments.payment_method="cashondelivery"
      payments.save()
      orders = order(user=user,order_id=order_id_generated,address=addresss,total=amount,date=dates)
      orders.payment=payments
      orders.save()
      carts_item = cart_item.objects.filter(
                 user=request.user, is_active=True
             ).order_by("id")
      for x in carts_item:
         orderproduct = order_product(order=orders,user=user)
         orderproduct.quantity =x.quantity
         orderproduct.product=x.product
         orderproduct.payment=payments
         orderproduct.product_price=x.product.price
         orderproduct.save() 
         product = products.objects.get(id = x.product.id)
         product.stock -= x.quantity
         product.save()
      orderss=order.objects.filter(order_id =order_id_generated)
      ordered_products =order_product.objects.filter(order=orders)
      carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
      
      total=0
      quantity=0
      tax=0
      for item in carts_item:
         total += offer_check(item) * item.quantity
         quantity += item.quantity
      carts_item.delete()
      if reduction > 0:
        new_total= total-reduction*total/100
      else:
        new_total=total
      if "coupon_code" in request.session:
        try:
            coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
            coupon_useduser.save()
        except:
            pass
   else:
      return redirect()
   context = {
            "payments":payments,
            "order":orders,
            "ordered_products":ordered_products,
            "orderID":order_id_generated,
            "addresss":addresss,
            # "transID":order_id_generated,
            "dates":dates,
            "total":total,
            "tax":tax,
            "total":total,
            "quantity":quantity,
            "new_total":new_total  
        }
   if "coupon_code" in request.session:
        del request.session["coupon_code"] 
   return render (request,"order_conforme.html",context)
   return HttpResponse ("Payment success thanks for the order")
    
   return render (request,"order_conforme.html",context)
   

#---------------------------------------------------------------------------------------\razopay/---------------------------------------------------------------------------------------------------



# authorize razorpay client with API Keys.
# def razorpay(request):
#    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#    payment = client

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def razorpay_sucess(request):
   # order_id = request.GET.get("order_id")
   cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
   cart_itemcount = cart_items.count()
   if cart_itemcount <= 0 :
        return redirect ("index_page")

   if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
   else:
        reduction = 0
   user =request.user
   carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
   
   total=0
   quantity=0
   for item in carts_item:
      total += offer_check(item) * item.quantity
      quantity += item.quantity
   if reduction > 0:
        new_total= total-reduction*total/100
   else:
        new_total=total
   order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   dates =date.today()
   amount = new_total
   payment_method="razorpay"
   payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
   payments = payment(user=user,payment_id=payment_id,payment_method=payment_method,amount=amount,date=dates)
   payments.save()
   orders = order(user=user,order_id=order_id_generated,address=addresss,total=new_total,date=dates,payment=payments)
   orders.save()
   ordered_products = order_product.objects.filter(order = orders)

   cart_items  = cart_item.objects.filter(user = request.user)
   for x in cart_items:
        print(orders)       
        Orderproduct = order_product(order=orders)
        Orderproduct.user=user
        Orderproduct.payment=payments
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.product_price = offer_check(x)
        Orderproduct.save()
   if "coupon_code" in request.session:
        try:
            coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
            coupon_useduser.save() 
        except:
            pass
   carts_item.delete()
   if "coupon_code" in request.session:
        del request.session["coupon_code"] 
   context = {
            "payments":payments,
            "order":orders,
            "ordered_products":ordered_products,
            "orderID":orders.order_id,
            "addresss":addresss,
            "transID":order_id_generated,
            "dates":dates,
            "total":total,
            "total":new_total,
            "quantity":quantity,
            "reduction":reduction,
            "new_total":new_total
   }
   return render (request,"order_conforme.html",context)

   return HttpResponse ("Payment success thanks for the order")
   













# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# def paypal(request):
#     total = 0
#     quantity = 0
#     cart_items =None
#     tax = 0
#     grand_total =0
#     if request.user.is_authenticated:
#         try:

#             details = address.objects.get(id = address_id ) #passed that spesific address in the details variable
#             order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
#             user =  request.user
#             cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
#             cart_itemcount = cart_items.count()
#             if cart_itemcount <= 0 :
#                 return render(request,'nothing.html')
#             for carts_item in cart_items:
#                 total += (int(carts_item.product.price) * int(carts_item.quantity))
                
#             oder = order(user=user,address=details ,total = total,order_id =order_id_generated)
#             oder.save()

            
#             cart_items  = cart_item.objects.filter(user = request.user, is_active = True)

            
            

#         except ObjectDoesNotExist: 
#             pass #just ignore

        
        

#     else:
#         return redirect(cart_view)
        
#     orders = order.objects.get(order_id = order_id_generated)
#     Orderproduct = order_product.objects.filter(order=orders)
#     for cart_items in Orderproduct:
#         total += (cart_items.price * cart_items.quantity)
#         quantity += cart_item.quantity
#     # tax = (2*total)/100
#     tax = 0
#     grand_total = total + tax
            
#     context = {
#     'cart_items':cart_items,
#     'order' :order,
#     "order_id_generated" :order_id_generated,
#     'total':total,
#     'quantity':quantity,
#     'Orderproduct':Orderproduct,
#     'tax':tax,
#     'grand_total':grand_total,
#     'details':details,
        
#         }
#     return render(request, 'paypal.html',context)
    



# def payments(request):
#     body = json.loads(request.body)
#     orders = order.objects.get(orderid = body['orderID'] )
#     payments = payment(

#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = orders.ordertotal,
#         status = body['status'],
#     )
#     payments.save()
#     print(body)
#     orders.payment = payment
#     orders.is_ordered =True
#     orders.save()
#     #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
#     cart_items  = cart_item.objects.filter(user = request.user, is_active = True)
#     for x in cart_items:
                
#         Orderproduct = order_product(order=order)
#         Orderproduct.product = x.product
#         Orderproduct.quantity = x.quantity
#         Orderproduct.product_price = x.product.price
#         Orderproduct.save()
#     #REDUCE THE QUANTITY OF STOCK

#         product = product.objects.get(id = x.product.id)
#         product.stock -= x.quantity
#         product.save()
#     #CLEAR CART
#     for x in cart_items:
#         x.delete()

#     #SEND ORDER RECIEVED EMAIL TO CUSTOMER




#     #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
#     data = {
#         "orderID":order.orderid,
#         "transID":payment.payment_id,
#     }


#     return JsonResponse(data)




# def order_complete(request):
#     total = 0
#     quantity = 0
#     cart_items =None
#     tax = 0
#     grand_total =0
#     order_number    = request.GET.get("orderID")
#     transID         = request.GET.get("transID")
#     print(order_number)

#     try:
#         dates =date.today()   
#         details = address.objects.get(id = address_id )
#         orders = order.objects.get(orderid = order_number)
#         ordered_products = order_product.objects.filter(order = orders)
#         Orderproduct = order_product.objects.filter(order=orders)
#         for cart_item in Orderproduct:
#             total += (cart_item.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         # tax = (2*total)/100
#         tax = 0
#         grand_total = total + tax

#         context = {
#             "order":orders,
#             "ordered_products":ordered_products,
#             "orderID":orders.orderid,
#             "details":details,
#             "transID":transID,
#             "dates":dates,
#             "grand_total":grand_total,
#             "tax":tax,
#             "total":total
#         }
#         return render(request,"order_complete.html",context)

#     except (payment.DoesNotExist,order.DoesNotExist):
#         return redirect("userhome")


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def paypal(request):
    # preview_page view
    if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
    else:
        reduction = 0
        
    if request.user.is_authenticated:
        try:
        
            carts_item = cart_item.objects.filter(
                user=request.user, is_active=True
            ).order_by("id")
            if not carts_item:
                return redirect ("index_page")

            cart_itemcount = carts_item.count()
            if cart_itemcount <= 0 :
                return redirect ("index_page")
                
            total=0
            quantity=0
      
            for item in carts_item:
                total += offer_check(item) * item.quantity
                quantity += item.quantity
            if reduction > 0:
                new_total= total-reduction*total/100
            else:
                new_total=total
            
            order_id_generated = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            dates =date.today()
            orders = order(user=request.user,address=addresss ,total = new_total,order_id =order_id_generated,date=dates)
            order_products = order_product.objects.filter(order=orders)
            orders.save()
        except ObjectDoesNotExist:
               pass #just ignore
    else:
        return redirect(cart_view)
   
   
    values ={"carts_item":carts_item,"total":new_total,"quantity":quantity,"orders":orders,"order_products":order_products,}
   
    return render (request,"paypal.html",values)

# ///////////////////////////////////////////////////////////////////////////////////


def payments(request):
    user=request.user
    # if request.session.get('posted_page_visited'):
    #     del request.session['posted_page_visited']
    #     # return http.HttpResponseRedirect("form_page")
    #     return HttpResponse ("Payment success thanks for the orderaaa")
    body = json.loads(request.body)
    print(body['orderID'])

    orders = order.objects.get( order_id = body['orderID'] )
    payments = payment(

        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount = orders.total,
        # status = body['status'],
    )
    payments.save()
    print(body)
    print(orders.order_id)
    # print(orders.payments.payment_id)

    orders.payment = payments
    orders.is_ordered =True
    orders.save()
    print(orders)       


    #MOVE THE CART ITEMS TO ORDER PRODUCTS TABLE
    cart_items  = cart_item.objects.filter(user = request.user)
    print(cart_items)
    for x in cart_items:
        print(orders)       
        Orderproduct = order_product(order=orders)
        print(Orderproduct)
        Orderproduct.user=user
        Orderproduct.product = x.product
        Orderproduct.quantity = x.quantity
        Orderproduct.product_price = offer_check(x)
        Orderproduct.save()
    #REDUCE THE QUANTITY OF STOCK

        product = products.objects.get(id = x.product.id)
        product.stock -= x.quantity
        product.save()
    #CLEAR CART
    for x in cart_items:
        x.delete()

    #SEND ORDER RECIEVED EMAIL TO CUSTOMER
    



    #SEND ORDER NUMBER AND TRANSACTION ID BACK TO SEND DATA METHOD VIA JASON RESPONDS
    data = {
        "orderID":orders.order_id,
        "transID":payments.payment_id,
    }

    return JsonResponse(data)


@cache_control(no_cache =True, must_revalidate =True, no_store =True)   
def order_complete(request):
    user =request.user
    total = 0
    quantity = 0
    cart_items =None
    tax = 0
    grand_total =0
    order_number    = request.GET.get("orderID")
    transID         = request.GET.get("transID")
    print(order_number)
    if "coupon_code" in request.session:
        coupons =coupon.objects.get(coupon_code =request.session["coupon_code"])
        reduction =coupons.discount_percentage
    else:
        reduction = 0
    try:
        dates =date.today()  

        addresss = address.objects.get(id = address_id )
        payment_method = "paypal"
        
        payments = payment(user=request.user,payment_id=order_number,payment_method=payment_method,amount=grand_total,date=dates)
        payments.save()
        orders = order.objects.get(order_id = order_number)
        orders.payment=payments
        orders.save()

        ordered_products = order_product.objects.filter(order = orders)
        print(ordered_products)
        

        print(ordered_products)
        for cart_item in ordered_products:
            total += (offer_check(cart_item) * cart_item.quantity)
            quantity += cart_item.quantity
            cart_item.payment=payments
            cart_item.save()
        # tax = (2*total)/100
        tax = 0
        grand_total = total + tax
        if reduction > 0:
            new_total= total-reduction*total/100
        else:
            new_total=total
       
       
        print(orders)
        context = {
            "payments":payments,
            "order":orders,
            "ordered_products":ordered_products,
            "orderID":orders.order_id,
            "addresss":addresss,
            "transID":transID,
            "dates":dates,
            "total":total,
            "tax":tax,
            "total":new_total,
            "quantity":quantity,
            "reduction":reduction,
            "new_total":new_total
            
        }
        # request.session['posted_page_visited'] = True
        if "coupon_code" in request.session:
            try:
                coupon_useduser=couponuseduser(coupon=coupons,user=request.user)
                coupon_useduser.save()
            except:
                pass
        if "coupon_code" in request.session:
            del request.session["coupon_code"] 


    #   return render(request,"index.html" )
        return render (request,"order_conforme.html",context)

    except (payment.DoesNotExist,order.DoesNotExist):
                 return redirect ("index_page")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def order_cancel(request,id):
   user =request.user
   if request.user.is_authenticated:
      orders = order.objects.get(id=id)
      orders.status= "cancelled"
      orders.save()
      orderproduct=order_product.objects.filter(order=orders)   
      orderproduct.product_status="cancelled"
      orderproduct.save()
      if orders.payment.payment_method == "cashondelivery":
            pass
      else:
        wallets=wallet.objects.get(user=user)
        wallets.balance = orders.total
      
      for x in orderproduct:
         product = products.objects.get(id =x.product.id) 
         product.stock += x.quantity
         product.save()
        
   return redirect(user_profile)

def product_order_cancel(request,id):
    users =request.user
    if request.user.is_authenticated:
      orderproduct=order_product.objects.get(id=id)
      orderproduct.product_status = "cancelled"
      orderproduct.save()
      if orderproduct.payment.payment_method == "cashondelivery":
            pass

      else:
        wallets=wallet.objects.get(user=users)
        wallets.balance += orderproduct.product_price*orderproduct.quantity
        print(wallets.balance)
        wallets.save()
      producte = products.objects.get(id =orderproduct.product.id) 
      producte.stock += orderproduct.quantity
      producte.save()
    return redirect(user_profile)

def product_return(request,id):
       if request.user.is_authenticated:
            dates = date.today()  
      
            # orders=order.objects.get(id=id)
            order_products=order_product.objects.get(id=id)
            # order_date=order_products.order.date 
            # order_products =order_product(product_status="return_accepted")
            order_products.product_status = "return_accepted"

            order_products.save()
            # orders=order(status="return_accepted")
            # orders.save()
            if order_products.payment.payment_method == "cashondelivery":
                pass

            else:
                try:
                    wallets=wallet.objects.get(user=request.user)
                    wallets.balance += order_products.product_price*order_products.quantity
                    print(wallets.balance)
                    wallets.save()
                except:
                    pass
            # for x in order_products:
            product = products.objects.get(id =order_products.product.id) 
            product.stock += order_products.quantity
            product.save()
                    

            return redirect(user_profile)
