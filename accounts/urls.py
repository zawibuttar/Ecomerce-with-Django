from django.urls import path
from accounts.views import  initiate_payment,logout_user,login_page, register_page, activate_email,cart,add_to_cart,remove_coupon,remove_from_cart,update_cart
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('login/',login_page,name="login"),
    path('register/' , register_page , name="register"),
    path('activate/<email_token>/',activate_email,name='activate_email'),
    path('logout/',logout_user,name='logout'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('update_cart/',update_cart,name="update_cart"),
    path('cart/',cart,name="cart"),
    path('remove_from_cart/<str:id>/',remove_from_cart,name="remove_from_cart"),
    path('remove_coupon/<cart_id>/',remove_coupon,name="remove_coupon"),
    path('payment/initiate/', initiate_payment, name='initiate_payment'),


    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]