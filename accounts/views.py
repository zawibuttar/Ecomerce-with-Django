from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login
from .models import Profile,Add_To_Cart,ShoppingCart
from myapp.models import product,Coupon




def login_page(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=em)
        except User.DoesNotExist:
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=em, password=password)
        if user_obj:
            if not user_obj.profile.is_email_verified:
                messages.warning(request, 'Your account is not verified.')
                return HttpResponseRedirect(request.path_info)

            login(request, user_obj)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Invalid credentials.')
            return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')


def register_page(request):

  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_obj = User.objects.filter(username=email)
    if user_obj.exists():
          messages.warning(request, 'Email is already taken.')
          return HttpResponseRedirect(request.path_info) #request.path_info is used to redirect the user to the same URL they are currently accessing.
    user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
    user_obj.set_password(password)
    user_obj.save()

    messages.success(request, 'An email has been sent on your mail.')
    return HttpResponseRedirect(request.path_info)

  return render(request,'accounts/register.html')

def activate_email(request,email_token):
  try:
    user=Profile.objects.get(email_token=email_token)
    user.is_email_verified=True
    user.save()
    return redirect('/')
  except Exception as e:
    return HttpResponse('invalid email Token')
  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
# from django.views.decorators.http import require_POST

# class Myserial(serializers.ModelSerializer):
#     class Mete:
#         model=add_to_cart
#         fields=['user','product_id','selected_size','item_price','item_color','quantity']
@csrf_exempt
@api_view(["POST"])
def add_to_cart(request):
    if request.user.is_authenticated:
        try:
            # dat = json.loads(request.body)
            dat = request.data    #Using request.data instead of json.loads(request.body) is recommended when working with Django REST Framework because request.data is a higher-level abstraction provided by the framework.
            size = dat.get('size', None)
            q = dat.get('quantity', None)
            c = dat.get('color', None)
            p = dat.get('price')
            pid = dat.get('pid')
            product_obj = product.objects.get(uid=pid)
            obj1 = ShoppingCart.objects.create(user=request.user)

            obj=Add_To_Cart.objects.create(product=product_obj,shopping_cart=obj1,item_color=c,selected_size=size,item_price=p,quantity=q)

            return Response({"my": "Done"}, status=status.HTTP_200_OK)
        except:
            return Response({"my": "NotDone"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"link":"accounts/login/"},status=status.HTTP_401_UNAUTHORIZED)
  
def cart(request):
   cart_obj = ShoppingCart.objects.get(user=request.user, is_paid=False)
   if request.method=="POST":
       coupon=request.POST.get('coupon')
       coup_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
       if not coup_obj.exists():
           messages.warning(request,'invalid Coupon')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       if cart_obj.coupon:
           messages.warning(request,"Coupon Already Exists")
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       # if  > Coupon.minimum_amount:
       #     messages.warning(request, f"Amount should be greater than {Coupon.minimum_amount}")
       #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

       cart_obj.coupon=coup_obj[0]
       cart_obj.save()
       messages.success(request, "Coupon applied")
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   cart_obj = ShoppingCart.objects.filter(user=request.user, is_paid=False)
   if request.user.is_authenticated:
    # cart_obj=ShoppingCart.objects.filter(user=request.user,is_paid=False)
    count = cart_obj.count()
    for cart_item in cart_obj:
        cart_item.total_items_price = cart_item.total_items_price()
        print(cart_item.total_items_price)
        for item in cart_item.addtocart.all():
            print(f"  Product: {item.product.product_name}, Size: {item.selected_size}, Quantity: {item.quantity}, Price: {item.item_price}")

   else:
       return redirect('/accounts/login/')

   return render(request,"product/cart.html",{'cart':cart_obj,'count':count})


@api_view(['POST'])
def update_cart(request):
    try:
        # Extract data from the request
        dat = request.data
        uid = dat.get('uid')
        quantity = dat.get('quantity')
        print("myid",uid)


        # Validate uid and quantity
        if not uid or not quantity:
            return Response({"error": "Both uid and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert uid to string (if necessary) and retrieve the cart item
        cart_item = Add_To_Cart.objects.get(uid=str(uid))

        # Update quantity and save the cart item
        cart_item.quantity = quantity
        cart_item.save()

        # Calculate total price
        total_price = cart_item.item_price * quantity

        # Return successful response with total price
        return Response({"total_price": total_price}, status=status.HTTP_200_OK)

    except Add_To_Cart.DoesNotExist:
        # Handle case where the cart item does not exist
        return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Handle generic exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def remove_from_cart(request,id):
    print(id)
    obj=ShoppingCart.objects.get(uid=id)
    obj.delete()

    return HttpResponseRedirect('/accounts/cart/')
