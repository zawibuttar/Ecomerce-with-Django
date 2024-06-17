from django.db import models
from Base.models import BaseModel
from django.utils.text import slugify
class category(BaseModel):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to='categories')

    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(category,self).save(*args,**kwargs)
    def __str__(self):
        return self.category_name


class ColorVariant(BaseModel):
    color_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    def __str__(self):
        return self.color_name

class SizeVariant(BaseModel):
    size_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    def __str__(self):
        return self.size_name
    
class product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name='products')
    price = models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)
    product_description = models.TextField()
    color_variant=models.ManyToManyField(ColorVariant,blank=True)
    size_variant=models.ManyToManyField(SizeVariant,blank=True)
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super(product,self).save(*args,**kwargs)
    def __str__(self):
        return self.product_name
    def price_calulate_size(self,size):
        return self.price+SizeVariant.objects.get(size_name=size).price

class ProductImage(BaseModel):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to='product')

class Coupon(BaseModel):
    coupon_code= models.CharField(max_length=20)
    is_expired =models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=1000)
    def __str__(self):
        return self.coupon_code
