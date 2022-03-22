from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic import View

from . import models


# Create your views here.
class ListProducts(ListView):
    template_name = 'produto/list.html'
    model = models.Product
    context_object_name = 'produtos'
    paginate_by = 10


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
