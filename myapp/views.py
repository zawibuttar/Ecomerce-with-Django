from django.shortcuts import render
from myapp.models import product

def get_products(request,slug):
    obj=product.objects.get(slug=slug)

    return render(request,'product/products.html',{'product':obj})
# Create your views here.
