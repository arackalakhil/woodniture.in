from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import re

from pkg_resources import require
from carts.models import categoryoffer, coupon, couponuseduser, productoffer
from order.models import order, order_product, payment
from products.models import banner, products, categories
from django.db.models import Sum,Count
from datetime import date
import datetime
import users
from users.models import address, customuser

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signin_admins(request):
    if "username" in request.session:
        return redirect(dashboard)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user is not None and user.is_superuser:

            request.session["username"] = email
            login(request, user)
            return redirect(dashboard)
        else:
            messages.error(request, "Enter correct admin deatils")
            return redirect(signin_admins)

    return render(request, "adminlogin.html")


# def home_admin(request):
#     if "username" in request.session:
#         return render(request, "adminindex.html")


def user_data_table(request):
    values= None
    if "username" in request.session :
        values = customuser.objects.all()
    return render(request, "user_data_table.html", {"values": values})

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signout_admin(request):
    if "username" in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin_admins)


def list_products(request):
    if "username" in request.session:
        values = products.objects.all()
        return render(request, "admin_products.html", {"values": values})


def category_products(request):
    # if 'username' in request.session:
    values = categories.objects.all()

    return render(request, "cat_products.html", {"values": values})


# def delete_user(request,id):
#     del_user = User.objects.get(id=id)
#     del_user.delete()
#     return redirect(user_data_table)

# def update_user(request,id):
#     obj =  User.objects.get(id = id )
#     if request.method == "POST":
#         username = request.POST.get('username')
#         name = request.POST.get('name')
#         emailid = request.POST.get('email')
#         obj.first_name = username
#         obj.name = name
#         obj.email = emailid
#         obj.save()
#         return redirect(user_data_table)
#     return render(request,'update_user.html',{'user':obj})


def delete_products(request, id):
    delete_product = products.objects.get(id=id)
    delete_product.delete()
    return redirect(list_products)


def update_products(request, id):
    objs = products.objects.get(id=id)
    values = categories.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        des = request.POST.get("des")
        img = request.POST.get("img")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        cat = request.POST.get("cat")
        # stocks=int(stock)

        if name == "":
            messages.error(request, " product name is empty")
            return render(request, "update_products.html", {"products": objs, "values": values})
            

        elif len(name) < 2:
                messages.error(request, "product name is too short")
                return render(request, "update_products.html", {"products": objs, "values": values})

                
        elif products.objects.filter(name=name):
                messages.error(request, " product name exits")
                return render(request, "update_products.html", {"products": objs, "values": values})
                
                
        # elif des == "":
        #         messages.error(request, "des field is empty")
        #         return render(request, "add_products.html")
        elif price == "":
            messages.error(request, "price is empty")
            return render(request, "update_products.html", {"products": objs, "values": values})
            
        elif stock ==" ":
            messages.error(request, "stock is empty")
            return render(request, "update_products.html", {"products": objs, "values": values})

            

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')    
        try:
            obj = products.objects.get(id=id)
            obj.name = name
            obj.des = des
            obj.img = img
            obj.price = price
            obj.stock = stock
            obj.cat = cat
            obj.save()
            return redirect(list_products)
        except:
            messages.error(request, "enter correct data")
            return render(request, "update_products.html", {"products": objs, "values": values})
            
        
    return render(request, "update_products.html", {"products": objs, "values": values})


def add_products(request):
    values = categories.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        des = request.POST.get("des")
        img = request.POST.get("img")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        cat = request.POST.get("cat")
        # stocks=int(stock)
        if name == "":
            messages.error(request, " product name is empty")
            return render(request, "add_products.html", {"values": values})

        elif len(name) < 2:
                messages.error(request, "product name is too short")
                return render(request, "add_products.html", {"values": values})
                
        elif products.objects.filter(name=name):
                messages.error(request, " product name exits")
                return render(request, "add_products.html", {"values": values})
                
        # elif des == "":
        #         messages.error(request, "des field is empty")
        #         return render(request, "add_products.html")
        elif price == "":
            messages.error(request, "price is empty")
            return render(request, "add_products.html")
        elif stock == " ":
            messages.error(request, "stock is empty")
            return render(request, "add_products.html", {"values": values})
            

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')    
        try:
            product = products(name=name, des=des, img=img, price=price, stock=stock)
            product.cats = categories.objects.get(id=cat)
            product.save()
            return redirect(list_products)
        except:
            messages.error(request, "enter correct data")
            return render(request, "add_products.html", {"values": values})
    return render(request, "add_products.html", {"values": values})


def add_category(request):

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        des = request.POST.get("des")
        stock = request.POST.get("stock")

        if category_name == "":
            messages.error(request, " category name is empty")
            return render(request, "add_category.html")
        elif des =="":
            messages.error(request, " add description ")
            return render(request, "add_category.html")
        elif stock =="":
            messages.error(request, " stock is empty ")
            return render(request, "add_category.html")
        try:
            category = categories(category_name=category_name, des=des, stock=stock)
            category.save()
            return redirect(category_products)
        except:
            messages.error(request, "stock is empty")
            return render(request, "add_category.html")
    return render(request, "add_category.html")


def delete_category(request, id):
    del_category = categories.objects.get(id=id)
    del_category.delete()
    return redirect(category_products)


def update_category(request, id):

    obj = categories.objects.get(id=id)
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        des = request.POST.get("des")
        stock = request.POST.get("stock")
        offer = request.POST.get("offer")
        if category_name == "":
            messages.error(request, " category name is empty")
            return render(request, "update_category.html", {"categories": obj})

        elif des =="":
            messages.error(request, " add description ")
            return render(request, "update_category.html", {"categories": obj})
            
        elif stock =="":
            messages.error(request, " stock is empty ")
            return render(request, "update_category.html", {"categories": obj})

        try:
            values = categories.objects.get(id=id)
            values.name = category_name
            values.des = des
            values.stock = stock
            values.offer = offer
            values.save()
            return redirect(category_products)
        except:
            messages.error(request, "stock is empty")
            return render(request, "update_category.html", {"categories": obj})

    return render(request, "update_category.html", {"categories": obj})


def block_user(request, id):
    user = customuser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(user_data_table)

def order_management(request):
    if "username" in request.session:
        orderproduct=order_product.objects.all().order_by("id")
        orders = order.objects.all().order_by("id")
        return render(request,"order_management.html",{"orderproduct":orderproduct,"orders":orders})  

def change_status(request,id):
    if "username" in request.session:
        if request.method == "POST":
            status = request.POST.get("status")
            orders = order.objects.get(id=id)
            orders.status= status
            print(status)
            orders.save()
            return redirect(order_management)


def product_order_management(request,id):
    if "username" in request.session:
        orders = order.objects.get(id=id)
        orderproduct=order_product.objects.filter(order=orders)
        return render(request,"product_order_management.html",{"orderproduct":orderproduct,"orders":orders})  
        
def product_change_status(request,id):
    if "username" in request.session:
        if request.method == "POST":
            status = request.POST.get("status")
            orderproduct = order_product.objects.get(id=id)
            orderproduct.status= status
            print(status)
            orderproduct.save()
            return redirect(order_management)          



def add_product_offer(request):
    product =products.objects.all().order_by("id")
    if request.method == "POST":
        # valid_from = request.POST.get("valid_from")
        # valid_to = request.POST.get("valid_to")
        discount = request.POST.get("discount")
        producte = request.POST.get("product")
        
        try:
            discount=int(discount)
            if discount > 0 :
                if discount < 90: 
                    productoffers = productoffer( discount=discount)
                    productoffers.product = products.objects.get(id=producte)
                    productoffers.save()
                    return redirect(product_offer_view)

        except:
            messages.success(request," offer must be between 1 to 90%")
            return render(request, "add_offer.html", {"values": product})

    return render(request, "add_offer.html", {"values": product})

def product_offer_view(request):
    productoffers = productoffer.objects.all().order_by("-id")
    return render(request, "product_offer.html", {"values": productoffers})

def block_product_offer(request, id):
    productoffers = productoffer.objects.get(id=id)
    if productoffers.is_active:
        productoffers.is_active = False
    else:
        productoffers.is_active = True
    productoffers.save()
    return redirect(product_offer_view)
def delete_product_offers(request,id):
    productoffers = productoffer.objects.get(id=id)
    productoffers.delete()
    return redirect(product_offer_view)

def edit_product_offer(request,id):
    productoffers = productoffer.objects.get(id=id)
    product=products.objects.all()
    if request.method == "POST":
        # valid_from = request.POST.get("valid_from")
        # valid_to = request.POST.get("valid_to")
        discount = request.POST.get("discount")
        # producte = request.POST.get("product")
        print(discount)
        discount=int(discount)
        try:
            if discount > 0 :

                if discount < 90:  

                    productoffers = productoffer.objects.get(id=id)
                    productoffers.discount= discount

                    productoffers.is_active=True
                    # productoffers.product = products.objects.get(id=producte)
                    productoffers.save()
                    return redirect(product_offer_view)
        except:
            messages.success(request,"offer must be between 1 to 90%")
            return render(request, "edit_offer.html", {"values": product,"productoffers":productoffers})
    return render(request, "edit_offer.html", {"values": product,"productoffers":productoffers})




def add_category_offer(request):
    categorie =categories.objects.all().order_by("id")
    if request.method == "POST":
        # valid_from = request.POST.get("valid_from")
        # valid_to = request.POST.get("valid_to")
        discount = request.POST.get("discount")
        cats = request.POST.get("product")
        try:
            discount=int(discount)

            if discount > 0 :
                if discount < 90: 
                    categoryoffers = categoryoffer( discount=discount)
                    categoryoffers.category = categories.objects.get(id=cats)
                    categoryoffers.save()
                    return redirect(category_offer_view)

        except:
            messages.success(request," offer must be between 1 to 90%")
            return render(request, "add_category_offer.html", {"values": categorie})

    return render(request, "add_category_offer.html", {"values": categorie})

def category_offer_view(request):
    categoryoffers  = categoryoffer.objects.all().order_by("-id")
    return render(request, "category_offer.html", {"values": categoryoffers})

def block_category_offer(request, id):
    categoryoffers = categoryoffer.objects.get(id=id)
    if categoryoffers.is_active:
        categoryoffers.is_active = False
    else:
        categoryoffers.is_active = True
    categoryoffers.save()
    return redirect(category_offer_view)
def delete_category_offers(request,id):
    categoryoffers = categoryoffer.objects.get(id=id)
    categoryoffers.delete()
    return redirect(category_offer_view)

def edit_category_offer(request,id):
    
    categoryoffers = categoryoffer.objects.get(id=id)
    categorie =categories.objects.all().order_by("id")

    if request.method == "POST":
        # valid_from = request.POST.get("valid_from")
        # valid_to = request.POST.get("valid_to")
        discount = request.POST.get("discount")
        # producte = request.POST.get("product")
        print(discount)
        discount=int(discount)
        try:
            if discount > 0 :

                if discount < 90:  

                    categoryoffers = categoryoffer.objects.get(id=id)
                    categoryoffers.discount= discount

                    categoryoffers.is_active=True
                    # productoffers.product = products.objects.get(id=producte)
                    categoryoffers.save()
                    return redirect(category_offer_view)
        except:
            messages.success(request,"offer must be between 1 to 90%")
            return render(request, "edit_offer.html", {"values": categorie,"categoryoffers":categoryoffers})
    return render(request, "edit_offer.html", {"values": categorie ,"categoryoffers":categoryoffers})

def view_coupon(request):
    coupons =coupon.objects.all().order_by("id")
    return render(request, "view_coupon.html",{"coupons":coupons})
def view_couponuseduser(request):
    coupon_useduser=couponuseduser.objects.all().order_by("id")
    return render(request, "view_couponuseduser.html",{"coupon_useduser:coupon_useduser"})

# def add_coupon(request):
#     if request.method == "POST":
#         coupon_code =request.POST.get("coupon_code")
#         discount_price =request.POST.get("discount_price")
#         coupons=coupon(coupon_code=coupon_code,discount_price=discount_price)
#         coupons.save()
#     return request(view_coupon)

def add_coupon(request):
    if request.method == "POST":
        coupon_code =request.POST.get("coupon_code")
        discount_percentage =request.POST.get("discount_price")
        
        try:
            discount= int(discount_percentage)
            if discount > 0 :
                if discount <100:
                    coupons=coupon(coupon_code=coupon_code,discount_percentage=discount)
                    coupons.save()
                    return redirect(view_coupon)
        except:
            messages.success(request,"cant repeat same coupon and offer must be between 1 to 90%")
            return render(request, "add_coupon.html")
                     
    return render(request, "add_coupon.html")
         

def block_coupon(request, id):
    coupons = coupon.objects.get(id=id)
    if coupons.is_active:
        coupons.is_active = False
    else:
        coupons.is_active = True
    coupons.save()
    return redirect(view_coupon)


def delete_coupon(request,id):
    coupons = coupon.objects.get(id=id)
    coupons.delete()
    return redirect(view_coupon)

    
def dashboard(request):
    orders = order.objects.all()
    # orderproduct = OrderProduct.objects.filter(product__category_name = 1)
    

    codtotal = payment.objects.filter(payment_method = 'cashondelivery').aggregate(Sum('amount')).get('amount__sum')
    cod = payment.objects.filter(payment_method = 'cashondelivery').aggregate(Count('id')).get('id__count')
       
    raztotal = payment.objects.filter(payment_method = 'razorpay').aggregate(Sum('amount')).get('amount__sum')
    raz = payment.objects.filter(payment_method = 'razorpay').aggregate(Count('id')).get('id__count')

    paytotal = payment.objects.filter(payment_method = 'Paypal').aggregate(Sum('amount')).get('amount__sum')
    pay = payment.objects.filter(payment_method = 'Paypal').aggregate(Count('id')).get('id__count')

    ordertotal = payment.objects.all().aggregate(Sum('amount')).get('amount__sum')

    context = {
            'orders':orders,
            'codtotal':codtotal,
            'paytotal':paytotal,
            'raztotal':raztotal,
            'total':ordertotal,
            'pay':pay,
            'raz':raz,
            'cod':cod
        }
    print(paytotal)
    return render(request, "adminindex.html",context)

def salesreport(request):
    salesreport = order.objects.filter(is_ordered = True).order_by('-id')
    
    if request.method  == 'POST':
        search = request.POST["salesreport_search"]
        salesreports = order.objects.filter(order_id__contains = search)
        context = {
            'salesreport':salesreports
        }
        return render (request,"salesreport.html",context)
   
    context = {
            'salesreport':salesreport
        }
    return render (request,"salesreport.html",context)


def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]

            salesreport = order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]) ,is_ordered =True)

            context = {
                'salesreport':salesreport,
            }

            return render(request,'salesreport.html',context)

        else:
            salesreport = order.objects.all()
            context = {
                'salesreport': salesreport ,

             }
            


    return render (request,"salesreport.html",context)
        


def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]

    salesreport = order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')

def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    salesreport = order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]),is_ordered =True).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')

    
# def orderdetails(request):
#      orders = order.objects.all()
#      addresss = address.objects.all()
#      order_products = order_product.objects.all()
#      return render(request,"orderdetails.html",{"orders":orders,"address":addresss,"order_products":order_products})  




# def sales_report(request):
#     salesreport = Order.objects.all().order_by('-created_at')
#     total = 0
#     total= salesreport.aggregate(Sum('order_total')).get('order_total__sum')
#     RoundTotal =("{:0.2f}".format(total))

    
#     p           = Paginator(salesreport, 10)
#     page_num  = request.GET.get('page')
#     try:
#         page        = p.page (page_num)
#     # except EmptyPage:
#     #     page        = p.page(1)
#     except PageNotAnInteger:
#         page        = p.page(1)

    
#     context = {
        
#         # 'salesreport': salesreport,
#         'RoundTotal': RoundTotal,
#         'items':page,

#     }
#     return render(request,'adm/sales_report.html',context)




# def monthly_report(request,date):
#     context = None
#     frmdate = date
   
#     fm = [ 2022 , frmdate , 1 ]
#     todt = [2022 , frmdate , 28 ]
    
#     print(fm)
            
#     salesreport = Order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
    
#     if len(salesreport) > 0 :   
#         context = {
#                 'salesreport' : salesreport ,  
               
#             }
#         print(salesreport)
#         print("Showing monthly Orders")
#         return render(request,'adm/search_report_sales.html',context)
#     else:
#         print("Showing No monthly Orders")
#         messages.error(request, "No orders in this month")
#     return render(request,'adm/sales_report.html',context)






# def yearly_report(request,date):
#     context = None
#     frmdate = date
   
#     fm = [ frmdate , 1 , 1 ]
#     todt = [frmdate , 12 , 30 ]
    
#     print(fm)
            
#     salesreport = order.objects.filter(created_at__gte=datetime.date(fm[0],fm[1],fm[2]), created_at__lte=datetime.date(todt[0],todt[1],todt[2])).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).annotate(sum=Sum('order_total')).order_by('-day')
#     if len(salesreport) > 0 :   
#         context = {
#                 'salesreport' : salesreport ,   
#             }
#         print(salesreport)
#         print("Showing yearly Orders")
#         return render(request,'adm/search_report_sales.html',context)
#     else:
#         print("No Orders")
#         messages.info(request,"No Orders")
#     return render(request,'adm/sales_report.html',context)

def adds_banners(request):
    if request.method == "POST":
        img = request.POST.get('img')
        title = request.POST.get('title') 
        description=request.POST.get("description")
        if img == " ":
            messages.error(request,"image field is empty")
            return redirect(view_banner)
        if title == "" or len(title)< 2:
            messages.error(request,"title field is empty")
            return redirect(view_banner)
        if description == "" or len(description)< 2:
            messages.error(request,"description field is empty")
            return redirect(view_banner)

        banners=banner(img=img,title=title,description=description)
        banners.save()
        return redirect(view_banner)

    return render(request,"add_banner.html")

def view_banner(request):
    banners=banner.objects.all()
    return render(request,"view_banners.html",{"banners":banners})

def update_banner(request,id):
    banners=banner.objects.get(id=id)
    if request.method == "POST":
        img = request.POST.get('img')
        title = request.POST.get('title') 
        description=request.POST.get("description")
        if img == " ":
            messages.error(request,"image field is empty")
            return render(request, "add_banner.html")
        if title == "" or len(title)< 2:
            messages.error(request,"title field is empty")
            return render(request, "add_banner.html")
        if description == "" or len(description)< 2:
            messages.error(request,"description field is empty")
            return render(request, "add_banner.html")
        try:
            banners=banner.objects.get(id=id)
            banners.img=img
            banners.title=title
            banners.description=description
            banners.save()
            return redirect(view_banner)
        except:
            pass
    return render(request, "add_banner.html", {"banners": banners})
def block_banner(request,id):
    banners=banner.objects.get(id=id)
    if banners.is_selected == True :
        banners.is_selected = False
        banners.save()

    else:
        banners.is_selected = True
        banners.save()
    return redirect(view_banner)
def delete_banner(request,id):
    banners=banner.objects.get(id=id)
    banners.delete()
    return redirect(view_banner)

def user_search(request):
    values=None 
    searchvalue =None
    if request.method == "POST":
        searchvalue = request.POST.get('search')
        try:
            values = customuser.objects.get(email__icontains = searchvalue)
            return render(request,"user_data_table.html",{"values":values})
        except:
            return render(request,"user_data_table.html")

