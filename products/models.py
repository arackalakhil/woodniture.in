
from pydoc import describe
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class categories(models.Model):
    category_name = models.CharField(max_length = 300)
    des = models.TextField()
    stock = models.IntegerField(null=True)
    # offer = models.IntegerField(null=True)
    # category_new_price = models.IntegerField(null=True)
    def __str__(self):
        return self.category_name

class products(models.Model):
    name = models.CharField(max_length=300,null=True)
    des = models.TextField(null=True)
    # img = models.ImageField(null=True,upload_to = "product_images")
    img = models.CharField(max_length=3000,null=True)
    price = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    cats = models.ForeignKey(categories,on_delete=models.CASCADE,null=True,blank=True)
    # product_new_price =models.IntegerField(null=True)
     
    def __str__(self):
        return self.name
    

class banner(models.Model):
    img = models.CharField(max_length=3000,null=True)
    title= models.CharField(max_length=300,null=True)
    description = models.TextField(null=True)
    is_selected=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    # def offer_price(self):
    #     if self.offerproduct:
    #         if self.categories.offer > self.offerproduct:
    #             return self.price - self.price *(self.categories.offer/100)

    #         else:
    #             return self.price-self.price*(self.offerproduct/100)
    #     else:
    #         return self.price -self.price*(self.categories.offer/100)

