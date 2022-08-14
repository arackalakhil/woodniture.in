from email.headerregistry import Address
from re import T
from tkinter import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumbers import country_code_for_region

# Create your models here.


class Myaccountmanager(BaseUserManager):
    def create_user(
        self, first_name, last_name, username, email, phone_number, password=None
    ):
        if not email:
            raise ValueError("user must have an email id")
        if not username:
            raise ValueError("user must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(
        self, first_name, last_name, email, phone_number, username, password
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class customuser(AbstractBaseUser):
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=250, unique=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    objects = Myaccountmanager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class address(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    address_details = models.CharField(max_length=300, blank=True)
    pincode = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class userprofile(models.Model):
    user = models.ForeignKey(customuser,on_delete=models.CASCADE)
    Address =models.CharField(max_length=100,blank=True)
    town = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
     
    def __str__(self):
        return self.user.username



    
class wallet(models.Model):
    user = models.ForeignKey(customuser,on_delete=models.CASCADE)
    balance = models.FloatField( max_length=15, null = True, default= 0 )
    is_applied = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username
