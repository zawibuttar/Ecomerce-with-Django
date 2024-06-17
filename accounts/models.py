from django.db import models
from django.contrib.auth.models import User
from myapp.models import product,Coupon
from Base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from Base.emails import send_account_activation_email
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

@receiver(post_save, sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email=instance.email
            send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)

class ShoppingCart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)

    # def get_cart_total(self):
    #    cart_items = self.cart_items.all()
    #
    #    price = []
    #    for cart_item in cart_items:
    #     price.append(cart_item.product.price)
    #     if cart_item.color_variant:
    #      color_variant_price = cart_item.color_variant.price
    #      price.append(color_variant_price)
    #     if cart_item.size_variant:
    #      size_variant_price = cart_item.size_variant.price
    #      price.append(size_variant_price)
    #    return sum(price)

    def total_items_price(self):
        return sum(item.total_price() for item in self.addtocart.all())

class Add_To_Cart(BaseModel):
     # user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='addcart')
     product=models.ForeignKey(product, on_delete=models.CASCADE)
     shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE,related_name="addtocart")
     selected_size=models.CharField(max_length=30)
     item_price=models.FloatField()
     item_color=models.CharField(max_length=30 ,blank=True,null=True)
     quantity=models.IntegerField()
     def total_price(self):
         return self.item_price * self.quantity
     def __str__(self):
        return self.product.product_name


# class Cart(BaseModel):
#     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
#     coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
#     is_paid=models.BooleanField(default=False)