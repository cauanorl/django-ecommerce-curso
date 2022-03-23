from django.shortcuts import render, get_object_or_404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from . import models


# Create your views here.
class ListProducts(ListView):
    template_name = 'produto/list.html'
    model = models.Product
    context_object_name = 'produtos'
    paginate_by = 10


class ProductDetails(DetailView):
    template_name = 'produto/details_product.html'
    model = models.Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'variations': models.Variation.objects.filter(
                product__slug=self.kwargs.get('slug')
            ),
        })
        return context
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)


class AddToCart(View):
    pass


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
