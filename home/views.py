from django.shortcuts import render
from myapp.models import product
from accounts.models import ShoppingCart
# Create your views here.
def index(request):
    context={'products': product.objects.all()}
    if request.user.is_authenticated:
      cart_items=ShoppingCart.objects.filter(user=request.user)
      cart_item_count= cart_items.count()
      context['count']=cart_item_count
    else:
        context['count'] = 0
    return render(request,'home/index.html',context)