from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic import View

# Create your views here.
class ListProducts(ListView):
    pass


class ProductDetails(View):
    pass


class AddToCart(View):
    pass


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
