from django.shortcuts import render
from myapp.models import product
# Create your views here.
def index(request):
    return render(request,'home/index.html',{'products': product.objects.all()})