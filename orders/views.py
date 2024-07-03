from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse,redirect
from .models import OrderPlaced
from myapp.models import product
from accounts.models import Profile,Add_To_Cart,ShoppingCart
import uuid
from django.contrib import messages
def order(request):
    cartItems=ShoppingCart.objects.filter(user=request.user,is_paid=False)
    count=cartItems.count()
    obj=OrderPlaced.objects.filter(customer=request.user)
    paid,unpaid=OrderPlaced.CalcuatePayments(obj)
    oc=obj.count()
    return render(request,'order/orderhistory.html',{"orders":obj,"total_amount_spent":paid+unpaid,"total_paid":paid,"orders_count":oc,"count":count})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
@api_view(["POST"])
@csrf_exempt
def BuySingleProduct(request):
    if request.user.is_authenticated:
        try:
            # dat = json.loads(request.body)
            dat = request.data
            size = dat.get('size')
            q = dat.get('quantity', None)
            c = dat.get('color', None)
            p = dat.get('price')
            pid = dat.get('pid')
            print("single",c,p,q,pid)

            if size==None:
                return Response({"message": "please select the size"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("here")
                product_obj = product.objects.get(uid=pid)
                print(product_obj.product_name)
                obj1=ShoppingCart.objects.create(user=request.user,is_paid=True)
                print("shop",obj1)
                obj = Add_To_Cart.objects.create(
                    product=product_obj,
                    shopping_cart=obj1,
                    item_color=c,
                    selected_size=size,
                    item_price=p,
                    quantity=q
                )
                amount=(p*q)+250
                print(amount)
                obj_order=OrderPlaced.objects.create(customer=request.user,total_amount=amount,order=obj1)

                return Response({"link":"/orders/history/","message": "Your Order is placed successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Unfortunately! Your Order is not placed due to some technical Error"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"link":"accounts/login/"},status=status.HTTP_401_UNAUTHORIZED)

def ViewOrderdetails(request,cart_id):
    CartCountItems = []
    try:
        CartObjectUnpaid = ShoppingCart.objects.get(user=request.user, is_paid=False)
        CartCountItems = Add_To_Cart.objects.filter(shopping_cart=CartObjectUnpaid)
        CountItems = CartCountItems.count()
    except ShoppingCart.DoesNotExist:
        CartObjectUnpaid = None
        CartCountItems = []
        CountItems = 0



    cart=ShoppingCart.objects.get(uid=cart_id,user=request.user)
    orderhistory=OrderPlaced.objects.get(order=cart)
    print(orderhistory.Is_order_delivered)
    cartitems=Add_To_Cart.objects.filter(shopping_cart=cart)
    count=cartitems.count()
    discount=orderhistory.calculateDiscount(cart)
    cart_Total_price=cart.get_cart_total()+discount
    context = {'discount':discount,
               'count':CountItems,
               'Count':count,
               'Cart':cart,
               'cart':cartitems,
               'cart_total':cart_Total_price,
               'order_history':orderhistory,
               }
    return render(request,"order/viewOrderDetails.html",context=context)

# def renderr(request):
#
#     return render(request,"order/order_invoice_email.html")