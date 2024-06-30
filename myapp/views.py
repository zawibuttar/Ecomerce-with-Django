from django.shortcuts import render,redirect, HttpResponse
from myapp.models import product
from accounts.models import Add_To_Cart,ShoppingCart
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def get_products(request,slug):
    obj=product.objects.get(slug=slug)
    context = {'product': obj}
    if request.user.is_authenticated:

      try:
            cart_obj = ShoppingCart.objects.get(user=request.user, is_paid=False)
      except ShoppingCart.DoesNotExist:
            cart_obj = None
      cart_items=Add_To_Cart.objects.filter(shopping_cart=cart_obj)
      cart_item_count= cart_items.count()
      context['count']=cart_item_count
    else:
        context['count'] = 0

    if request.GET.get('size'):
        size=request.GET.get('size')
        context['selected_size']=size
        updated_price = obj.price_calulate_size(size=size)
        context['updated_price']=updated_price
    return render(request,'product/products.html',context=context)



