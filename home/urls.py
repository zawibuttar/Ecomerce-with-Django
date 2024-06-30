from django.urls import path
from home.views import index,search_view
urlpatterns = [
    path('',index,name="index"),
    path('search/<slug:slug>/', search_view, name='search'),
    path('search/', search_view, name='search'),

]