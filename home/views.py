from django.shortcuts import render
from myapp.models import product
from accounts.models import ShoppingCart,Add_To_Cart
from django.db.models import Q
# Create your views here.
def index(request):
    context={'products': product.objects.all()}
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
    return render(request,'home/index.html',context)
def search_view(request,slug=None):
    if not slug==None:
      context = {'products': product.objects.filter(
            Q(product_name__icontains=slug) |
            Q(slug__icontains=slug) |
            Q(category__category_name__icontains=slug) |
            Q(product_description__icontains=slug))}
      if request.user.is_authenticated:
          cart_items = ShoppingCart.objects.filter(user=request.user)
          cart_item_count = cart_items.count()
          context['count'] = cart_item_count
      else:
          context['count'] = 0
      return render(request, 'home/index.html', context)
    else:
      context = {'products': product.objects.all()}
      if request.user.is_authenticated:
          cart_items = ShoppingCart.objects.filter(user=request.user)
          cart_item_count = cart_items.count()
          context['count'] = cart_item_count
      else:
          context['count'] = 0
      return render(request, 'home/index.html', context)



