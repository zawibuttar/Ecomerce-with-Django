from django.urls import path
from myapp.views import get_products

urlpatterns = [
    path('<slug>/',get_products,name="get_product"),
    # path('add_to_cart/',add_to_cart,name='add_to_cart')

]