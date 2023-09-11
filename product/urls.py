from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('add_to_cart/',add_to_cart, name='add_to_cart'),
    path('update_cart/',update_cart,name='update_cart'),
    path('remove_from_cart/',remove_from_cart,name='remove_from_cart'),
    path('load_cart_items/',load_cart_items,name='load_cart_items'),
    path('checkout/',checkout_page,name='checkout')
]