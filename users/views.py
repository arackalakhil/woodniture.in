import code
from multiprocessing import AuthenticationError, context
import numbers
import optparse
import random
from urllib.request import Request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.test import Client
from carts.models import cart, cart_item
from django.contrib import auth
from carts.views import cart_id, checkout
from order.models import order, order_product
from .models import address, customuser, wallet
from django.views.decorators.cache import cache_control
import re
from twilio.rest import Client
from datetime import date
from products.views import index_page
from django.conf import settings


# def index(request):
#     return render(request,'index.html')
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signin(request):
    if "username" in request.session:
        return redirect(index_page)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
    
        if user is not None:
            try:
                carts = cart.objects.get(cart_id=cart_id(request))
                carts_item = cart_item.objects.filter(cart = carts) 
                users_item = cart_item.objects.filter(user = user)

                for x in carts_item:#if multiple item in cart 
                    a=0
                    if users_item:
                            for y in users_item:#check each items in users_items 
                                if  x.product == y.product:#if product in both carts_items from sessions id and users  product from cart_item(models) matches
                                    y.quantity += x.quantity#product items quantity will be sum of .....
                                    x.delete()#delete the carts_item  
                                    y.save()
                                    a=1
                                    break
                                if a==0:# to add if different product to user cart 
                                    x.user=user
                                    x.save()
                    else:
                        x.user=user
                        x.save()

            except:
                pass    
            login(request, user)
            request.session["username"] = email
            return redirect(index_page)
        else:
            messages.success(request, "Enter correct deatils")
            return redirect(signin)
    return render(request, "login-register.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if username == "":
                messages.error(request, "username is empty")
                return render(request, "user-register.html")
            elif len(username) < 2:
                messages.error(request, "username is too short")
                return render(request, "user-register.html")
            elif not username.isalpha():
                messages.error(request, "username must contain alphabets")
                return render(request, "user-register.html")
            elif not username.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return render(request, "user-register.html")
            elif customuser.objects.filter(username=username):
                messages.error(request, "username exits")
                return render(request, "user-register.html")
            elif email == "":
                messages.error(request, "email field is empty")
                return render(request, "user-register.html")
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return render(request, "user-register.html")
  
            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif customuser.objects.filter(email=email):
                messages.error(request, "email already exist try another")
                return render(request, "user-register.html")

            else:
                user1 = customuser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1,
                    email=email,
                    phone_number=phone_number,
                )
                user1.save()
                wallets=wallet(user=user1)
                wallets.balance=0
                wallets.save()
                return redirect(signin)
        else:
            messages.success(request, "password does not match")
            return render(request, "user-register.html")
    else:
        return render(request, "user-register.html")

    return render(request, "user-register.html")

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signout(request):
    if "username" in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin)


# -------------------------------------------#OTP----------------------------------------------------------
# def numb_login(request):
#     if request.user.is_authenticated:
#         return redirect(index_page)
#     if request.method == "POST":
#         mobile = "8138873820"
#         phone_number = request.POST.get("phone_number")
#         # global numb
#         # numb = phone_number
#         # # if customuser.objects.filter(phone_number=phone_number):
#         # print(phone_number )
#         if mobile == phone_number:
#             # SID Twilio
#             account_sid = "AC18894f6eab9a08b51d59cda6416a4f08"
#             # auth Twilio
#             auth_token = "a41263d1c638186fc8ac618802ba6916"

#             client = Client(account_sid, auth_token)
#             global opt
#             opt = str(random.randint(1000, 9999))
#             message = client.messages.create(
#                 # to = "int((str(+91))+(str(phone_number)))",
#                 to="+918138873820",
#                 from_="+19705089552",
#                 body="greeting from woodniture your OTP is " + opt,
#             )

#             # return render(request,'otp.html')
#             return redirect(otp)
#         else:
#             messages.info(request, "invalid number")
#             return redirect(numb_login)

#     return render(request, "phone_login.html")


# def otp(request):
#     if request.method == "POST":
#         user = customuser.objects.get(phone_number=8138873820)
#         otpvalue = request.POST.get("otp")
#         if otpvalue == opt:
#             login(request, user)
#             messages.success(request, "logged in")
#             return redirect(index_page)
#         else:
#             messages.error(request, "incorrect OTP")
#             return render(otp)
#     else:
#         return render(request, "otp.html")
        

# -------------------------------------------#OTP----------------------------------------------------------
def number_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        phone_no="+91" + phone_number

        if customuser.objects.filter(phone_number=phone_number).exists():
            user = customuser.objects.get(phone_number = phone_number)
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid,auth_token)
            verification = client.verify \
                .services(settings.SERVICES) \
                .verifications \
                .create(to=phone_no ,channel='sms')
            return render(request,'otp.html',{'phone_number':phone_number})
            
            

        else:
            messages.info(request,'invalid Mobile number')
            return redirect(number_login)

    return render(request,"phone_login.html")


def otp(request,phone_number):
    if request.method == 'POST':
        if customuser.objects.filter(phone_number=phone_number):
            user      = customuser.objects.get(phone_number=phone_number)
            phone_no = "+91" + str(phone_number)
            otp_input   = request.POST.get('otp')

            if len(otp_input)>0:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)

                if verification_check.status == "approved":
                    # auth.login(request,user)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect(index_page)
                else:
                    messages.error(request,'Invalid OTP')
                    return render(request,'otp.html',{'phone_number':phone_number})

                   
            else:
                messages.error(request,'Invalid OTP')
                return render(request,'otp.html',{'phone_number':phone_number})

        else:

            messages.error(request,'Invalid Phone number')
            return redirect(otp)
    return render(request,"otp.html")































































































# /?//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def add_address(request):
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone_number = request.POST["phone_number"]
            user_address = request.POST["user_address"]
            country = request.POST["country"]
            town = request.POST["town"]
            state = request.POST["state"]
            zip_code = request.POST["zip_code"]

            if name == "":
                messages.error(request, "username is empty")
                return render(request, "add_address.html")
                

            elif len(name) < 2:
                messages.error(request, "username is too short")
                return render(request, "add_address.html")


            elif not name.isalpha():
                messages.error(request, "username must contain alphabets")
                return render(request, "add_address.html")


            elif not name.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return render(request, "add_address.html")
            elif address.objects.filter(name=name):
                messages.error(request, "username exits")

                return render(request, "add_address.html")
            elif email == "":
                messages.error(request, "email field is empty")
                return render(request, "add_address.html")
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return render(request, "add_address.html")

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            elif address.objects.filter(email=email):
                messages.error(request, "email already exist try another")
                return render(request, "add_address.html")

           
            address_data = address(
                    name=name,
                    email=email,
                    phone=phone_number,
                    address_details=user_address,
                    pincode=zip_code,
                    town=town,
                    state=state,
                    country=country,
                    user=request.user,
                )
            address_data.save()

            # return render(request, "checkout.html")

            return redirect(checkout)

        return render(request, "add_address.html")


def user_profile(request):
    
    if request.user.is_authenticated:
        user = request.user
        print(user)
        orders = order.objects.filter(user=user).order_by("-id")
        addresss =address.objects.filter(user=user).order_by("-id")
        order_products =order_product.objects.filter(user=user).order_by("-id")
        wallets=wallet.objects.get(user=user)
        user_data= customuser.objects.get(email=user)
        return render(request,"user_profile.html",{"orders":orders,"address":addresss,"order_products":order_products,"wallets":wallets,"user_data":user_data})  
    else:
        return redirect(index_page)

def user_order_details(request,id):
    if request.user.is_authenticated:
        user = request.user
        orders = order.objects.get(id=id)
        order_products = order_product.objects.filter(order=orders,user=user)

        return render(request,"user_order_details.html",{"order_products":order_products})  





def delete_address(request,id):
    if request.user.is_authenticated:
        del_address=address.objects.get(id=id)
        del_address.delete()
        return redirect(user_profile)
    else:
        return redirect(index_page)
        
def edit_address(request,id):
    values=address.objects.get(id=id)
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone_number = request.POST["phone_number"]
            user_address = request.POST["user_address"]
            country = request.POST["country"]
            town = request.POST["town"]
            state = request.POST["state"]
            zip_code = request.POST["zip_code"]
            addresss = address.objects.get(id=id)
            addresss.name=name,
            addresss.email=email,
            addresss.phone=phone_number,
            addresss.address_details=user_address,
            addresss.pincode=zip_code,
            addresss.town=town,
            addresss.state=state,
            addresss.country=country,
            # addresss.user=request.user
            if name == "":
                messages.error(request, "username is empty")
                return render(request, "edit_address.html")
                

            elif len(name) < 2:
                messages.error(request, "username is too short")
                return render(request, "edit_address.html")


            elif not name.isalpha():
                messages.error(request, "username must contain alphabets")
                return render(request, "edit_address.html")


            elif not name.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return render(request, "edit_address.html")
            elif address.objects.filter(name=name):
                messages.error(request, "username exits")

                return render(request, "edit_address.html")
            elif email == "":
                messages.error(request, "email field is empty")
                return render(request, "edit_address.html")
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return render(request, "edit_address.html")

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'edit_address.html')

            elif address.objects.filter(email=email):
                messages.error(request, "email already exist try another")
                return render(request, "edit_address.html")  
            addresss.save()
            return redirect(user_profile)
    return render(request,"edit_address.html",{"values":values})  

def add_new_address(request):
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone_number = request.POST["phone_number"]
            user_address = request.POST["user_address"]
            country = request.POST["country"]
            town = request.POST["town"]
            state = request.POST["state"]
            zip_code = request.POST["zip_code"]

            if name == "":
                messages.error(request, "username is empty")
                return render(request, "add_new_address.html")
                

            elif len(name) < 2:
                messages.error(request, "username is too short")
                return render(request, "add_new_address.html")


            elif not name.isalpha():
                messages.error(request, "username must contain alphabets")
                return render(request, "add_new_address.html")


            elif not name.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return render(request, "add_new_address.html")
            elif address.objects.filter(name=name):
                messages.error(request, "username exits")

                return render(request, "add_new_address.html")
            elif email == "":
                messages.error(request, "email field is empty")
                return render(request, "add_new_address.html")
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return render(request, "add_new_address.html")

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'add_new_address.html')

            # elif address.objects.filter(email=email):
            #     messages.error(request, "email already exist try another")
            #     return render(request, "add_new_address.html")           
            address_data = address(
                    name=name,
                    email=email,
                    phone=phone_number,
                    address_details=user_address,
                    pincode=zip_code,
                    town=town,
                    state=state,
                    country=country,
                    user=request.user,
                )
            address_data.save()

            # return render(request, "checkout.html")

            return redirect(user_profile)
        return render(request, "add_new_address.html")
def update_user(request,id):
    if request.user.is_authenticated:
        user =request.user
        if request.method == "POST":
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            phone_number = request.POST["phone_number"]
            # password =request.POST["password"]
            # password1 = request.POST["password1"]
            # password2 = request.POST["password2"]
            # if password1 == password2:
            if username == "":
                messages.error(request, "username is empty")
                return redirect(user_profile)
            elif len(username) < 2:
                messages.error(request, "username is too short")
                return redirect(user_profile)
            elif not username.isalpha():
                messages.error(request, "username must contain alphabets")
                return redirect(user_profile)
            elif not username.isidentifier():
                messages.error(request, "username start must start with alphabets")
                return redirect(user_profile)
            elif email == "":
                messages.error(request, "email field is empty")
                return redirect(user_profile)
            elif len(email) < 2:
                messages.error(request, "email is too short")
                return redirect(user_profile)

            # elif not re.fullmatch('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            #     messages.error(request,"email should contain @,.")
            #     return render(request,'signup.html')

            # elif customuser.objects.filter(email=email):
            #     messages.error(request, "email already exist try another")
            #     return redirect(user_profile)

            user1 =customuser.objects.get(id=id)
            old_number=user1.phone_number
            old_email=user1.email
            try:
                new_email=customuser.objects.exclude(email=old_email).filter(email=email)
                new_number=customuser.objects.exclude(phone_number=old_number).filter(phone_number=phone_number)
                if new_email == email or new_number == phone_number:
                    messages.error(request,"data existing")
                    return redirect(user_profile)
                elif old_email == email and old_number == phone_number:
                    user1.username=username
                    user1.first_name=first_name
                    user1.last_name=last_name
                    user1.save()
                    messages.success(request,"Data updated")
                    return redirect(user_profile)

                else:
                    user1.username=username
                    user1.first_name=first_name
                    user1.last_name=last_name
                    user1.email=email
                    user1.phone_number=phone_number
                    user1.save()
                    messages.success(request,"Data updated")
                    return redirect(user_profile)


            except:
                    messages.error(request,"data existing")

                    return redirect(user_profile)

def update_password(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            old_password =request.POST.get("old_password")
            new_password1=request.POST.get("new_password1")
            new_password2=request.POST.get("new_password2")
            user=request.user

            user1=customuser.objects.get(id=id)
            phone_number= user1.phone_number
            check =user.check_password(old_password)
            if check == True:
               
                if new_password1 != new_password2:
                    messages.error(request,"password dosent match")
                    return redirect(user_profile)
                if new_password1== "" or len(new_password1)<2:
                    messages.error(request,"Password to short")
                    return redirect(user_profile)

                else:
                    user.set_password(new_password1)
                    user.save()
                    users=customuser.objects.get(phone_number=phone_number)
                    login(request,users)
                    messages.success(request,"password updated")
                    return redirect(user_profile)

            else:
                messages.error(request,"password is wrong")
                return redirect(user_profile)

