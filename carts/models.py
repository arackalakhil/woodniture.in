from django.db import models
from django.forms import IntegerField

from products.models import categories, products
from users.models import customuser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class cart_item(models.Model): 
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    # couponx = models.ForeignKey(coupon,on_delete=models.SET_NULL, nulll =True,blank =True)
    
    def sub_total(self):
        return (
            self.product.price * self.quantity
        )  # self means we are refering to the model cart_item ,product is the foreignkey of porduct model inside the product model we have the price

    def __str__(self):
        return self.product.name



class productoffer(models.Model):
    product= models.OneToOneField(products,related_name='product_offer',on_delete=models.CASCADE)
    # valid_from = models.DateTimeField(null=True)
    # valid_to= models.DateTimeField(null=True)
    discount= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],null=True,default=0)
    is_active= models.BooleanField(default=True)
    def __str__(self):
        return self.product.name

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total

    

        

class categoryoffer(models.Model):
    category= models.OneToOneField(categories, related_name='cats_offers', on_delete=models.CASCADE)
    # valid_from = models.DateTimeField(null=True)
    # valid_to  = models.DateTimeField(null=True)
    discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):   
     return self.category.category_name



class coupon(models.Model):
    coupon_code = models.CharField(max_length=50,unique=True)
    discount_percentage = models.IntegerField(null=True)
    # discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    # discount_price = models.IntegerField(null=True)
    # minium_amount = models.IntegerField(null=True)
    def __str__(self):
        return self.coupon_code



class couponuseduser(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE,null=True)

    coupon = models.ForeignKey(coupon, on_delete=models.CASCADE,null=True)
    # count =models.CharField(max_length=20, null=True, blank=True)
   
   
   
    def __str__(self):
        return self.user.username