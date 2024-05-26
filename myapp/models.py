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

class product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name='products')
    price = models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)
    product_description = models.TextField()
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super(product,self).save(*args,**kwargs)
    def __str__(self):
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to='product')